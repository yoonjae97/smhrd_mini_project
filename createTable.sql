-- 음식점 : 1, 미용실 : 2, 학원 : 3, 기타 : 4, 인증 : 5 
-- 큰 테이블 :  1, review : 2, item : 3
-- 조합 = fk(게시판+테이블)

create table member (
mem_seq NUMBER not null primary key,
mem_id  varchar(200) NOT NULL,
mem_password    varchar(200) NOT NULL,
mem_google_id   varchar(200),
mem_naver_id    varchar(200),
mem_type    varchar(200) default 1 NOT NULL,
mem_age     number NOT NULL,
mem_name    varchar(200) NOT NULL,
mem_wdate   Date NOT NULL,
mem_update  Date
);
--drop SEQUENCE mem_seq;
--drop table member;
CREATE SEQUENCE mem_seq 
INCREMENT BY 1                                         
START WITH 1                                    
MINVALUE 1                                        
MAXVALUE 9999999999                  
NOCYCLE                                        
CACHE 20;   

--//레스토랑
create table restaurant (
res_seq NUMBER not null primary key,
mem_seq number not null,
res_name    VARCHAR(200) not null,
res_locate  varchar(200) not null,
res_phone   VARCHAR(200) not null,
res_content varchar(200),
res_score   NUMBER,
res_hit     NUMBER not null,
res_wdate   Date not null,
res_update  date,
CONSTRAINT fk11_mem_seq foreign key(mem_seq) references member (mem_seq)
);

CREATE SEQUENCE res_seq 
INCREMENT BY 1                                     
START WITH 1                                     
MINVALUE 1                                          
MAXVALUE 9999999999                        
NOCYCLE                                               
CACHE 20; 

create table res_review (
res_review_seq NUMBER not null primary key,
res_seq number not null,
res_review_title    varchar(200) not null,
res_review_content  varchar(200) not null,
res_review_wdate    date   not null,
res_review_rating   number not null,
CONSTRAINT fk12_res_seq foreign key(res_seq) references restaurant (res_seq)
);

CREATE SEQUENCE res_review_seq   
INCREMENT BY 1                                        
START WITH 1                                      
MINVALUE 1                                           
MAXVALUE 9999999999                              
NOCYCLE                                                 
CACHE 20;


create table res_item (
res_item_seq NUMBER not null primary key,
res_seq number not null,
res_item_title varchar(200) not null,
res_item_content varchar(200),
res_item_pic VARCHAR(200),
res_item_price NUMBER,
res_item_wdate Date not null,
res_item_update Date,
CONSTRAINT fk13_res_seq foreign key(res_seq) references restaurant (res_seq)
);

CREATE SEQUENCE res_item_seq  --시퀀스이름 SEQ_SER_SALEMAN_CNTL
INCREMENT BY 1                                         --증감숫자 1
START WITH 1                                      --시작숫자
MINVALUE 1                                               --최소값 1
MAXVALUE 9999999999                               --최대값 9999999999
NOCYCLE                                                   --순환하지않음
CACHE 20;

--beauty
create table beauty ( 
beauty_seq NUMBER not null primary key,
mem_seq number not null,
beauty_name VARCHAR(200) not null,
beauty_locate VARCHAR(200) not null,
beauty_phone VARCHAR(200) not null,
beauty_content VARCHAR(200),
beauty_score    number,
beauty_hit      number not null,
beauty_wdate    Date not null,
beauty_update   Date,
CONSTRAINT fk21_mem_seq foreign key(mem_seq) references member (mem_seq)
);

CREATE SEQUENCE beauty_seq   --시퀀스이름 SEQ_SER_SALEMAN_CNTL
INCREMENT BY 1                                         --증감숫자 1
START WITH 1                                      --시작숫자
MINVALUE 1                                               --최소값 1
MAXVALUE 9999999999                               --최대값 9999999999
NOCYCLE                                                   --순환하지않음
CACHE 20;

create table beauty_item (
beauty_item_seq  NUMBER not null primary key,
beauty_seq number not null,
beauty_item_title varchar(200) not null,
beauty_item_content varchar(200),
beauty_item_pic VARCHAR(200),
beauty_item_price NUMBER,
beauty_item_wdate Date not null,
beauty_item_update Date,
CONSTRAINT fk23_beauty_seq foreign key(beauty_seq) references beauty (beauty_seq)
);

CREATE SEQUENCE beauty_item_seq 
INCREMENT BY 1                                         --증감숫자 1
START WITH 1                                      --시작숫자
MINVALUE 1                                               --최소값 1
MAXVALUE 9999999999                               --최대값 9999999999
NOCYCLE                                                   --순환하지않음
CACHE 20;

create table beauty_review (
beauty_review_seq  NUMBER not null primary key,
beauty_seq number not null,
beauty_review_title varchar(200) not null,
beauty_review_content   varchar(200) not null,
beauty_review_wdate Date,
beauty_review_rating    NUMBER  not null,
CONSTRAINT fk22_beauty_seq foreign key(beauty_seq) references beauty (beauty_seq)
);

CREATE SEQUENCE beauty_review_seq
INCREMENT BY 1                                         --증감숫자 1
START WITH 1                                      --시작숫자
MINVALUE 1                                               --최소값 1
MAXVALUE 9999999999                               --최대값 9999999999
NOCYCLE                                                   --순환하지않음
CACHE 20;

create table etc (
etc_seq  NUMBER not null primary key,
mem_seq number not null,
etc_name varchar(200) not null,
etc_locate varchar(200) not null,
etc_phone varchar(200) not null,
etc_content varchar(200),
etc_score   NUMBER,
etc_hit     NUMBER not null,
etc_wdate   Date    not null,
etc_update  Date,
CONSTRAINT fk41_mem_seq foreign key(mem_seq) references member (mem_seq)
);

CREATE SEQUENCE etc_seq
INCREMENT BY 1                                         --증감숫자 1
START WITH 1                                      --시작숫자
MINVALUE 1                                               --최소값 1
MAXVALUE 9999999999                               --최대값 9999999999
NOCYCLE                                                   --순환하지않음
CACHE 20;

create table etc_item (
etc_item_seq  NUMBER not null primary key,
etc_seq number not null,
etc_item_title  varchar(200) not null,
etc_item_content varchar(200),
etc_item_pic    VARCHAR(200),
etc_item_price  NUMBER,
etc_item_wdate  Date    not null,
etc_item_update Date,
CONSTRAINT fk43_etc_seq foreign key(etc_seq) references etc (etc_seq)
);

CREATE SEQUENCE etc_item_seq
INCREMENT BY 1                                         --증감숫자 1
START WITH 1                                      --시작숫자
MINVALUE 1                                               --최소값 1
MAXVALUE 9999999999                               --최대값 9999999999
NOCYCLE                                                   --순환하지않음
CACHE 20;

create table etc_review (
etc_review_seq  NUMBER not null primary key,
etc_seq number not null,
etc_review_title varchar(200) not null,
etc_review_content varchar(200) not null,
etc_review_wdate Date not null,
etc_review_rating number not null,
CONSTRAINT fk42_etc_seq foreign key(etc_seq) references etc (etc_seq)
);

CREATE SEQUENCE etc_review_seq
INCREMENT BY 1                                         --증감숫자 1
START WITH 1                                      --시작숫자
MINVALUE 1                                               --최소값 1
MAXVALUE 9999999999                               --최대값 9999999999
NOCYCLE                                                   --순환하지않음
CACHE 20;

create table edu (
edu_seq  NUMBER not null primary key,
mem_seq number not null,
edu_name varchar(200) not null,
edu_locate varchar(200) not null,
edu_phone varchar(200) not null,
edu_content varchar(200),
edu_score   NUMBER,
edu_hit     NUMBER not null,
edu_wdate   Date    not null,
edu_update  Date,
CONSTRAINT fk31_mem_seq foreign key(mem_seq) references member (mem_seq)
);

CREATE SEQUENCE edu_seq
INCREMENT BY 1                                         --증감숫자 1
START WITH 1                                      --시작숫자
MINVALUE 1                                               --최소값 1
MAXVALUE 9999999999                               --최대값 9999999999
NOCYCLE                                                   --순환하지않음
CACHE 20;

create table edu_item (
edu_item_seq  NUMBER not null primary key,
edu_seq number not null,
edu_item_title  varchar(200) not null,
edu_item_content varchar(200),
edu_item_pic    VARCHAR(200),
edu_item_price  NUMBER,
edu_item_wdate  Date    not null,
edu_item_update Date,
CONSTRAINT fk33_edu_seq foreign key(edu_seq) references edu (edu_seq)
);

CREATE SEQUENCE edu_item_seq
INCREMENT BY 1                                       
START WITH 1                            
MINVALUE 1                                     
MAXVALUE 9999999999                           
NOCYCLE                                     
CACHE 20;

create table edu_review (
edu_review_seq  NUMBER not null primary key,
edu_seq number not null,
edu_review_title varchar(200) not null,
edu_review_content varchar(200) not null,
edu_review_wdate Date not null,
edu_review_rating number not null,
CONSTRAINT fk32_edu_seq foreign key(edu_seq) references edu (edu_seq)
);

CREATE SEQUENCE edu_review_seq
INCREMENT BY 1                                       
START WITH 1                            
MINVALUE 1                                     
MAXVALUE 9999999999                           
NOCYCLE                                     
CACHE 20;

create table authenticate (
authenticate_seq  NUMBER not null primary key,
mem_seq number not null,
auth_pic VARCHAR(200),
auth_wdate Date,
CONSTRAINT fk51_mem_seq foreign key(mem_seq) references member (mem_seq)
);

CREATE SEQUENCE authenticate_seq
INCREMENT BY 1                                       
START WITH 1                            
MINVALUE 1                                     
MAXVALUE 9999999999                           
NOCYCLE                                     
CACHE 20;


commit;