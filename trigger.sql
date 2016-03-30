USE dbcourse;

DELIMITER $$

CREATE TRIGGER order_detail_before_insert
BEFORE INSERT ON order_detail
FOR EACH ROW BEGIN
    DECLARE msg VARCHAR(255);
    DECLARE sid INT;
    DECLARE cur_qnt INT DEFAULT 0;

    SELECT shop_id INTO sid FROM orders WHERE orders.id = NEW.order_id LIMIT 1;
    SELECT quantity INTO cur_qnt FROM shop_detail WHERE detail_id = NEW.detail_id AND shop_id = sid LIMIT 1;
    IF (cur_qnt < NEW.quantity) THEN
        set msg = "[NO_ITEMS_IN_SHOP] There are no that much details of that kind in the shop!";
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
    END IF;

    IF (cur_qnt = NEW.quantity) THEN
        DELETE FROM shop_detail WHERE detail_id = NEW.detail_id AND shop_id = sid LIMIT 1;
    ELSE
        UPDATE shop_detail SET quantity = cur_qnt - NEW.quantity WHERE detail_id = NEW.detail_id AND shop_id = sid LIMIT 1;
    END IF;
END$$

CREATE TRIGGER order_detail_before_update
BEFORE UPDATE ON order_detail
FOR EACH ROW BEGIN
    DECLARE msg VARCHAR(255);
    DECLARE sid INT;
    DECLARE cur_qnt INT DEFAULT 0;

    SELECT shop_id INTO sid FROM orders WHERE orders.id = NEW.order_id LIMIT 1;
    SELECT quantity INTO cur_qnt FROM shop_detail WHERE detail_id = NEW.detail_id AND shop_id = sid LIMIT 1;
    IF (cur_qnt < NEW.quantity - OLD.quantity) THEN
        set msg = "[NO_ITEMS_IN_SHOP] There are no that much details of that kind in the shop!";
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
    END IF;

    IF (cur_qnt = NEW.quantity - OLD.quantity) THEN
        DELETE FROM shop_detail WHERE detail_id = NEW.detail_id AND shop_id = sid LIMIT 1;
    ELSE
        UPDATE shop_detail SET quantity = cur_qnt - NEW.quantity + OLD.quantity WHERE detail_id = NEW.detail_id AND shop_id = sid LIMIT 1;
    END IF;
END$$

CREATE TRIGGER order_detail_before_delete
BEFORE DELETE ON order_detail
FOR EACH ROW BEGIN
    DECLARE sid INT;
    DECLARE cur_qnt INT DEFAULT 0;

    SELECT shop_id INTO sid FROM orders WHERE orders.id = OLD.order_id LIMIT 1;
    SELECT quantity INTO cur_qnt FROM shop_detail WHERE detail_id = OLD.detail_id AND shop_id = sid LIMIT 1;
    IF (cur_qnt = 0) THEN
        INSERT INTO shop_detail (shop_id, detail_id, quantity)
            VALUES (sid, OLD.detail_id, OLD.quantity);
    ELSE
        UPDATE shop_detail SET quantity = quantity + OLD.quantity WHERE detail_id = OLD.detail_id AND shop_id = sid LIMIT 1;
    END IF;
END$$

CREATE TRIGGER order_detail_after_delete
AFTER DELETE ON order_detail
FOR EACH ROW BEGIN
    UPDATE orders SET price = (SELECT SUM(detail.price*order_detail.quantity)
        FROM order_detail INNER JOIN detail ON order_detail.detail_id = detail.id
        WHERE order_detail.order_id = OLD.order_id)
    WHERE orders.id = OLD.order_id;
END$$

CREATE TRIGGER order_detail_after_insert
AFTER INSERT ON order_detail
FOR EACH ROW BEGIN
    UPDATE orders SET price = (SELECT SUM(detail.price*order_detail.quantity)
        FROM order_detail INNER JOIN detail ON order_detail.detail_id = detail.id
        WHERE order_detail.order_id = NEW.order_id)
    WHERE orders.id = NEW.order_id;
END$$

CREATE TRIGGER order_detail_after_update
AFTER UPDATE ON order_detail
FOR EACH ROW BEGIN
    UPDATE orders SET price = (SELECT SUM(detail.price*order_detail.quantity)
        FROM order_detail INNER JOIN detail ON order_detail.detail_id = detail.id
        WHERE order_detail.order_id = NEW.order_id)
    WHERE orders.id = NEW.order_id;
END$$

CREATE TRIGGER detail_after_update
AFTER UPDATE ON detail
FOR EACH ROW BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE order_id INT;
    DECLARE cur CURSOR FOR SELECT DISTINCT orders.id FROM orders
            INNER JOIN order_detail ON orders.id = order_detail.order_id
            WHERE order_detail.detail_id = NEW.id;
    DECLARE CONTINUE HANDLER FOR SQLSTATE '02000' SET done = 1;

    OPEN cur;
    REPEAT
        FETCH cur INTO order_id;
        IF NOT done THEN
            UPDATE orders SET price = (SELECT SUM(detail.price*order_detail.quantity)
                FROM order_detail INNER JOIN detail ON order_detail.detail_id = detail.id
                WHERE order_detail.order_id = order_id)
            WHERE orders.id = order_id;
        END IF;
    UNTIL done END REPEAT;
END$$

DELIMITER ;