insert into t_product (name,price,number,introduce,big_img,small_img,state,cid_one,cid_two,cid_three,weight,hot_number,is_promote) value ('SOULKISS 高冷气质硬核款 16姆米桑蚕真丝双绉显瘦挂脖露肩连衣裙',879.99,100,'chanpin','','',2,1,17,75,100,30,1);
insert into t_product (name,price,number,introduce,big_img,small_img,state,cid_one,cid_two,cid_three,weight,hot_number,is_promote) value ('AmandaX定制重磅奢华真丝提花连肩袖小A连衣裙',879.99,100,'chanpin','','',2,1,17,75,100,30,1);
insert into t_product (name,price,number,introduce,big_img,small_img,state,cid_one,cid_two,cid_three,weight,hot_number,is_promote) value ('AmandaX定制30姆米2色重缎可调节V领吊带连衣裙',1380,100,'chanpin','','',2,1,17,75,100,30,1);
insert into t_product (name,price,number,introduce,big_img,small_img,state,cid_one,cid_two,cid_three,weight,hot_number,is_promote) value ('吊带连衣裙女2020夏季新款V领雪纺气质印花A字复古小碎花过膝长裙',359.00,100,'chanpin','','',2,1,17,75,100,30,1);
insert into t_product (name,price,number,introduce,big_img,small_img,state,cid_one,cid_two,cid_three,weight,hot_number,is_promote) value ('4/17拍 ^_^ 小婷版 温柔小姐姐 白色小花收腰长款连衣裙（20夏）',1399.99,100,'chanpin','','',2,1,17,75,100,30,1);
insert into t_product (name,price,number,introduce,big_img,small_img,state,cid_one,cid_two,cid_three,weight,hot_number,is_promote) value ('【思思法代】SANDRO 20春夏蕾丝镂空连衣裙女 SFPRO01010 R20568E',1386,100,'chanpin','','',2,1,17,75,100,30,1);


select t_category.level,count(1) from t_category group by level