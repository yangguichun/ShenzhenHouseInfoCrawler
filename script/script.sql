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
