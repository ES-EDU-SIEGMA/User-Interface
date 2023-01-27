--
-- PostgreSQL database dump
--

-- Dumped from database version 13.8 (Raspbian 13.8-0+deb11u1)
-- Dumped by pg_dump version 13.8 (Raspbian 13.8-0+deb11u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: beverage; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.beverage (
    id integer NOT NULL,
    name text NOT NULL,
    hopperid integer,
    flowspeed integer NOT NULL
);


ALTER TABLE public.beverage OWNER TO admin;

--
-- Name: beverage_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.beverage_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.beverage_id_seq OWNER TO admin;

--
-- Name: beverage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.beverage_id_seq OWNED BY public.beverage.id;


--
-- Name: hopper; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.hopper (
    id integer NOT NULL,
    "position" text NOT NULL
);


ALTER TABLE public.hopper OWNER TO admin;

--
-- Name: hopper_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.hopper_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.hopper_id_seq OWNER TO admin;

--
-- Name: hopper_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.hopper_id_seq OWNED BY public.hopper.id;


--
-- Name: mixeddrink; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.mixeddrink (
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.mixeddrink OWNER TO admin;

--
-- Name: mixeddrink_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.mixeddrink_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mixeddrink_id_seq OWNER TO admin;

--
-- Name: mixeddrink_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.mixeddrink_id_seq OWNED BY public.mixeddrink.id;


--
-- Name: recipe; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.recipe (
    id integer NOT NULL,
    beverageid integer NOT NULL,
    mixeddrinkid integer NOT NULL,
    fillingamount integer NOT NULL
);


ALTER TABLE public.recipe OWNER TO admin;

--
-- Name: recipe_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.recipe_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recipe_id_seq OWNER TO admin;

--
-- Name: recipe_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.recipe_id_seq OWNED BY public.recipe.id;


--
-- Name: beverage id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.beverage ALTER COLUMN id SET DEFAULT nextval('public.beverage_id_seq'::regclass);


--
-- Name: hopper id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.hopper ALTER COLUMN id SET DEFAULT nextval('public.hopper_id_seq'::regclass);


--
-- Name: mixeddrink id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.mixeddrink ALTER COLUMN id SET DEFAULT nextval('public.mixeddrink_id_seq'::regclass);


--
-- Name: recipe id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipe ALTER COLUMN id SET DEFAULT nextval('public.recipe_id_seq'::regclass);


--
-- Data for Name: beverage; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.beverage (id, name, hopperid, flowspeed) FROM stdin;
2	Apfelsaft	1	1
3	Orangensaft	2	1
4	Mineralwasser	3	1
6	Jaegermeister	5	1
7	Fanta	6	1
8	Coca Cola	7	1
9	Sprite	8	1
10	RedBull	9	1
11	Erdbeerschnaps	10	3
13	Zuckersirup	11	10
14	Limettensaft	12	1
16	Pfirsicheistee	\N	1
17	Zitroneneistee	\N	1
18	Bombay	\N	1
19	Jim Beam	\N	1
20	Jack Daniels	\N	1
21	Korn	\N	1
22	Gin	\N	1
23	Pfefferminzschnaps	\N	1
24	Waldmeisterschnaps	\N	1
25	Eierlikoer	\N	7
26	42er	\N	3
27	Milch	\N	2
28	Rum	\N	1
30	Bananensaft	\N	2
31	Multivitaminsaft	\N	2
32	Tequila	\N	2
33	Cointreau	\N	2
5	Vodka	\N	1
29	Kirschsaft	4	1
\.


--
-- Data for Name: hopper; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.hopper (id, "position") FROM stdin;
1	0
2	1
3	2
4	3
5	4
6	5
7	6
8	7
9	8
10	9
11	10
12	11
\.


--
-- Data for Name: mixeddrink; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.mixeddrink (id, name) FROM stdin;
1	Mojito
2	MezoMix
3	Korn Diesel
4	Korn Cola
5	Korn Fanta
6	Korn Sprite
7	VodkaO
8	VodkaE
9	Flying Hirsch
10	Vodka Cola
11	Vodka Fanta
13	Vodka Sprite
14	Vodka MezoMix
15	Apfelschorle
16	KiBa
17	LongIslandIceTee
\.


--
-- Data for Name: recipe; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.recipe (id, beverageid, mixeddrinkid, fillingamount) FROM stdin;
1	29	16	50
2	30	16	50
3	2	15	60
4	4	15	40
\.


--
-- Name: beverage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.beverage_id_seq', 33, true);


--
-- Name: hopper_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.hopper_id_seq', 12, true);


--
-- Name: mixeddrink_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.mixeddrink_id_seq', 17, true);


--
-- Name: recipe_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.recipe_id_seq', 4, true);


--
-- Name: beverage beverage_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.beverage
    ADD CONSTRAINT beverage_pkey PRIMARY KEY (id);


--
-- Name: hopper hopper_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.hopper
    ADD CONSTRAINT hopper_pkey PRIMARY KEY (id);


--
-- Name: mixeddrink mixeddrink_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.mixeddrink
    ADD CONSTRAINT mixeddrink_pkey PRIMARY KEY (id);


--
-- Name: recipe recipe_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipe
    ADD CONSTRAINT recipe_pkey PRIMARY KEY (id);


--
-- Name: beverage beverage_hopperid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.beverage
    ADD CONSTRAINT beverage_hopperid_fkey FOREIGN KEY (hopperid) REFERENCES public.hopper(id);


--
-- Name: recipe recipe_beverageid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipe
    ADD CONSTRAINT recipe_beverageid_fkey FOREIGN KEY (beverageid) REFERENCES public.beverage(id);


--
-- Name: recipe recipe_mixeddrinkid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipe
    ADD CONSTRAINT recipe_mixeddrinkid_fkey FOREIGN KEY (mixeddrinkid) REFERENCES public.mixeddrink(id);


--
-- PostgreSQL database dump complete
--

