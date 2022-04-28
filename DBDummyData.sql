
/* Product Table dummy data */
INSERT INTO EASYPEASY.`PRODUCT` (product_name, related_words, cost, live, measure, imageURL) VALUES ('Heineken', 'lager, beer' , 12.1, 1, 'Pint', 'https://www.countyengraving.co.uk/ekmps/shops/countyengraving/images/heineken-1-pint-glass-personalised-27701-1-p.jpg');

INSERT INTO EASYPEASY.`PRODUCT` (product_name, related_words, cost, live, measure, imageURL) VALUES ('Coke', 'soft drink, soft drinks, Coca-Cola, fizzy drink', 10, 1, 'Pint', 'https://i.dailymail.co.uk/i/pix/2013/02/12/article-2277388-051B79CC000005DC-289_306x433.jpg');

INSERT INTO EASYPEASY.`PRODUCT` (product_name, related_words, cost, live, measure, imageURL) VALUES ('Aperol', 'cocktail, cocktails', 5.2, 1, 'Glass', 'https://produits.bienmanger.com/30319-0w470h470_Aperol_Stemmed_Glass.jpg');

INSERT INTO EASYPEASY.`PRODUCT` (product_name, related_words, cost, live, measure, imageURL) VALUES ('Latte', 'hot drink, hot drinks, coffee', 4.2, 1, 'Cup', 'https://www.caffesociety.co.uk/assets/recipe-images/latte-small.jpg');

INSERT INTO EASYPEASY.`PRODUCT` (product_name, related_words, cost, live, measure, imageURL) VALUES ('White wine', 'wine, white wine', 1.1, 1, 'Glass', 'https://www.beeventhire.co.uk/wp-content/uploads/2019/01/25-cl-White-Wine-Glass.jpg');

INSERT INTO EASYPEASY.`PRODUCT` (product_name, related_words, cost, live, measure, imageURL) VALUES ('Prosecco', 'prosecco, fizzy drink', 7.4, 1, 'Bottle', 'https://www.bottlebutler.co.uk/wp-content/uploads/2016/03/Prosecco-1.jpg');

/* Language table dummy data */
INSERT INTO EASYPEASY.`LANGUAGE` (country, code, live, imageURL) VALUES ('Spain', 'es-ES', 1, 'https://cdn.britannica.com/36/4336-004-6BD81071/Flag-Spain.jpg');

INSERT INTO EASYPEASY.`LANGUAGE` (country, code, live, imageURL) VALUES ('United Kingdom', 'en-GB', 1, 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Flag_of_Great_Britain_%281707–1800%29.svg/1024px-Flag_of_Great_Britain_%281707–1800%29.svg.png');

INSERT INTO EASYPEASY.`LANGUAGE` (country, code, live, imageURL) VALUES ('France', 'fr-FR', 1, 'https://cdn.britannica.com/82/682-004-F0B47FCB/Flag-France.jpg');

INSERT INTO EASYPEASY.`LANGUAGE` (country, code, live, imageURL) VALUES ('Portugal', 'pt-PT', 1 , 'https://www.worldatlas.com/r/w1200/img/flag/pt-flag.jpg');

INSERT INTO EASYPEASY.`LANGUAGE` (country, code, live, imageURL) VALUES ('Croatia', 'hr-HR', 1 , 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Flag_of_Croatia.svg/1200px-Flag_of_Croatia.svg.png');

INSERT INTO EASYPEASY.`LANGUAGE` (country, code, live, imageURL) VALUES ('United States', 'en-US', 0 , 'https://cdn.britannica.com/33/4833-004-828A9A84/Flag-United-States-of-America.jpg');

INSERT INTO EASYPEASY.`LANGUAGE` (country, code, live, imageURL) VALUES ('Germany', 'de-DE', 0 , 'https://upload.wikimedia.org/wikipedia/en/thumb/b/ba/Flag_of_Germany.svg/800px-Flag_of_Germany.svg.png');

/* Admin login dummy data (The password is 'root' hashed with SHA256) */
INSERT INTO EASYPEASY.`ADMINLOGIN` (username, password) VALUES ('admin', '4813494d137e1631bba301d5acab6e7bb7aa74ce1185d456565ef51d737677b2');