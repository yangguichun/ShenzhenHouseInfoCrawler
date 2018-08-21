-- Table: public.newhousebyarea

-- DROP TABLE public.newhousebyarea;

--新房成交信息，按面积划分的信息
CREATE TABLE public.newhousebyarea
(
  thedate date NOT NULL,
  region character varying(255) NOT NULL,
  area_level character varying(255) NOT NULL,
  deal_count integer,
  area double precision,
  price double precision,
  total_price integer,
  CONSTRAINT newhousebyarea_primary_key PRIMARY KEY (thedate, region, area_level)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.newhousebyarea
  OWNER TO postgres;


-- Table: public.newhousebytype

-- DROP TABLE public.newhousebytype;

--新房成交信息，按类型划分
CREATE TABLE public.newhousebytype
(
  thedate date NOT NULL,
  region character varying(255) NOT NULL,
  house_type character varying(255) NOT NULL,
  deal_count integer,
  area double precision,
  price double precision,
  availableforsalecount integer,
  availableforsalearea integer,
  CONSTRAINT newhousebytype_primary_key PRIMARY KEY (thedate, region, house_type)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.newhousebytype
  OWNER TO postgres;



-- Table: public.newhousebyuse

-- DROP TABLE public.newhousebyuse;
--新房成交信息，按用途划分
CREATE TABLE public.newhousebyuse
(
  thedate date NOT NULL,
  region character varying(255) NOT NULL,
  use_type character varying(255) NOT NULL,
  deal_count integer,
  area double precision,
  price double precision,
  availableforsalecount integer,
  availableforsalearea integer,
  CONSTRAINT newhousebyuse_primary_key PRIMARY KEY (thedate, region, use_type)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.newhousebyuse
  OWNER TO postgres;


-- Table: public.oldhousebyuse

-- DROP TABLE public.oldhousebyuse;
--二手房成交信息，按用途划分
CREATE TABLE public.oldhousebyuse
(
  thedate date NOT NULL,
  region character varying(255) NOT NULL,
  use_type character varying(255) NOT NULL,
  area double precision,
  deal_count integer,
  CONSTRAINT oldhousebyuse_primary_key PRIMARY KEY (thedate, region, use_type)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.oldhousebyuse
  OWNER TO postgres;




-- Table: public.oldhousesource

-- DROP TABLE public.oldhousesource;
--二手房源信息
CREATE TABLE public.oldhousesource
(
  thedate date NOT NULL,
  region character varying(255),
  serial_num character varying(255) NOT NULL,
  project_name character varying(255) NOT NULL,
  area double precision,
  use_type character varying(255),
  code character varying(30),
  agency_info character varying(255),
  CONSTRAINT oldhousesource_primary_key PRIMARY KEY (serial_num)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.oldhousesource
  OWNER TO postgres;



-- Table: public.newhousesrc_project

-- DROP TABLE public.newhousesrc_project;
--新房的预售信息，项目信息
CREATE TABLE public.newhousesrc_project
(
  id serial NOT NULL, --id
  thedate date NOT NULL, --预售日期
  region character varying(255), --区域
  project_name character varying(255) NOT NULL, --项目名称
  builder character varying(255) NOT NULL, --开发商
  address character varying(255) NOT NULL, --地址
  house_useage character varying(255) NOT NULL, --房屋用途
  land_usage varchar(255),  --土地用途
  land_years_limit integer, --使用年限
  land_serial_num varchar(255), --土地宗地号
  land_contact_num varchar(255), --土地合同文号
  presale_license_num character varying(255) NOT NULL, --预售许可证
  pre_sale_count integer NOT NULL, -- 预售套数
  pre_area float,  --预售面积
  now_sale_count integer NOT NULL, -- 现售套数
  now_area float, --现售面积

  CONSTRAINT newhousesrc_project_primary_key PRIMARY KEY (id),
  CONSTRAINT newhousesrc_project_serial_num UNIQUE (presale_license_num)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.newhousesrc_project
  OWNER TO postgres;


-- Table: public.newhousesrc_building

-- DROP TABLE public.newhousesrc_building;
--新房预售信息，楼栋信息
CREATE TABLE public.newhousesrc_building
(
  id serial not null,
  project_id integer NOT NULL,
  project_name character varying(255) NOT NULL,
  building_name character varying(255) NOT NULL,
  plan_license character varying(255) NOT NULL,
  build_license character varying(255) NOT NULL,
  CONSTRAINT newhousesrc_building_primary_key PRIMARY KEY (id),
  CONSTRAINT newhousesrc_building_unique UNIQUE (project_id, building_name)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.newhousesrc_building
  OWNER TO postgres;


-- Table: public.newhousesrc_house

-- DROP TABLE public.newhousesrc_house;
-- 新房预售，每一套房屋的信息
CREATE TABLE public.newhousesrc_house
(
  id serial not null,
  building_id int not null,
  building_name character varying(255), --几栋
  branch character varying(10),   --座号
  room_num character varying(50),
  floor varchar(255),
  house_type character varying(255),
  contact_code character varying(255),
  price double precision,
  usage character varying(50),
  build_area double precision,
  inside_area double precision,
  share_area double precision,
  CONSTRAINT newhousesrc_house_primary_key PRIMARY KEY (id),
  CONSTRAINT newhousesrc_house_unique UNIQUE (building_id, branch, room_num)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.newhousesrc_house
  OWNER TO postgres;


--项目的简要信息，判断是否有新项目，以后后续的各种爬虫，都是基于这个来的
CREATE TABLE public.newhousesrc_project_summary
(
  id serial NOT NULL, --id
  thedate date NOT NULL, --预售日期
  region character varying(255), --区域
  presale_license_num varchar(255), --预售证
  project_name character varying(255) NOT NULL, --项目名称
  builder character varying(255) NOT NULL, --开发商
  url varchar(1024) NOT NULL,--项目的url
  is_crawled boolean,
  CONSTRAINT newhousesrc_project_summary_primary_key PRIMARY KEY (id),
  CONSTRAINT newhousesrc_project_summary_presale_license_num UNIQUE (presale_license_num)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.newhousesrc_project_summary
  OWNER TO postgres;
