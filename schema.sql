--
-- PostgreSQL database dump
--

-- Dumped from database version 14.1
-- Dumped by pg_dump version 14.1

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
-- Name: comments; Type: TABLE; Schema: public; Owner: niemijus
--

CREATE TABLE public.comments (
    id integer NOT NULL,
    user_id integer,
    recipe_id integer,
    content text,
    sent_at timestamp without time zone
);


ALTER TABLE public.comments OWNER TO niemijus;

--
-- Name: comments_id_seq; Type: SEQUENCE; Schema: public; Owner: niemijus
--

CREATE SEQUENCE public.comments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.comments_id_seq OWNER TO niemijus;

--
-- Name: comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: niemijus
--

ALTER SEQUENCE public.comments_id_seq OWNED BY public.comments.id;


--
-- Name: ingredients; Type: TABLE; Schema: public; Owner: niemijus
--

CREATE TABLE public.ingredients (
    id integer NOT NULL,
    name text,
    kcal integer,
    carbs double precision,
    protein double precision,
    fat double precision,
    salt double precision
);


ALTER TABLE public.ingredients OWNER TO niemijus;

--
-- Name: ingredients_id_seq; Type: SEQUENCE; Schema: public; Owner: niemijus
--

CREATE SEQUENCE public.ingredients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ingredients_id_seq OWNER TO niemijus;

--
-- Name: ingredients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: niemijus
--

ALTER SEQUENCE public.ingredients_id_seq OWNED BY public.ingredients.id;


--
-- Name: recipes; Type: TABLE; Schema: public; Owner: niemijus
--

CREATE TABLE public.recipes (
    id integer NOT NULL,
    name text,
    time_added date,
    total_cal integer,
    total_kcal double precision
);


ALTER TABLE public.recipes OWNER TO niemijus;

--
-- Name: recipes_id_seq; Type: SEQUENCE; Schema: public; Owner: niemijus
--

CREATE SEQUENCE public.recipes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recipes_id_seq OWNER TO niemijus;

--
-- Name: recipes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: niemijus
--

ALTER SEQUENCE public.recipes_id_seq OWNED BY public.recipes.id;


--
-- Name: recipes_ingredients; Type: TABLE; Schema: public; Owner: niemijus
--

CREATE TABLE public.recipes_ingredients (
    id integer NOT NULL,
    amount integer,
    recipe_id integer,
    ingredient_id integer
);


ALTER TABLE public.recipes_ingredients OWNER TO niemijus;

--
-- Name: recipes_ingredients_id_seq; Type: SEQUENCE; Schema: public; Owner: niemijus
--

CREATE SEQUENCE public.recipes_ingredients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recipes_ingredients_id_seq OWNER TO niemijus;

--
-- Name: recipes_ingredients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: niemijus
--

ALTER SEQUENCE public.recipes_ingredients_id_seq OWNED BY public.recipes_ingredients.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: niemijus
--

CREATE TABLE public.users (
    id integer NOT NULL,
    first_name text,
    last_name text,
    username text,
    password text,
    height integer,
    weight double precision,
    age integer,
    gender text,
    admin boolean,
    bmr double precision
);


ALTER TABLE public.users OWNER TO niemijus;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: niemijus
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO niemijus;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: niemijus
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: users_recipes; Type: TABLE; Schema: public; Owner: niemijus
--

CREATE TABLE public.users_recipes (
    id integer NOT NULL,
    user_id integer,
    recipe_id integer
);


ALTER TABLE public.users_recipes OWNER TO niemijus;

--
-- Name: users_recipes_id_seq; Type: SEQUENCE; Schema: public; Owner: niemijus
--

CREATE SEQUENCE public.users_recipes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_recipes_id_seq OWNER TO niemijus;

--
-- Name: users_recipes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: niemijus
--

ALTER SEQUENCE public.users_recipes_id_seq OWNED BY public.users_recipes.id;


--
-- Name: comments id; Type: DEFAULT; Schema: public; Owner: niemijus
--

ALTER TABLE ONLY public.comments ALTER COLUMN id SET DEFAULT nextval('public.comments_id_seq'::regclass);


--
-- Name: ingredients id; Type: DEFAULT; Schema: public; Owner: niemijus
--

ALTER TABLE ONLY public.ingredients ALTER COLUMN id SET DEFAULT nextval('public.ingredients_id_seq'::regclass);


--
-- Name: recipes id; Type: DEFAULT; Schema: public; Owner: niemijus
--

ALTER TABLE ONLY public.recipes ALTER COLUMN id SET DEFAULT nextval('public.recipes_id_seq'::regclass);


--
-- Name: recipes_ingredients id; Type: DEFAULT; Schema: public; Owner: niemijus
--

ALTER TABLE ONLY public.recipes_ingredients ALTER COLUMN id SET DEFAULT nextval('public.recipes_ingredients_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: niemijus
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: users_recipes id; Type: DEFAULT; Schema: public; Owner: niemijus
--

ALTER TABLE ONLY public.users_recipes ALTER COLUMN id SET DEFAULT nextval('public.users_recipes_id_seq'::regclass);


--
-- Name: comments comments_pkey; Type: CONSTRAINT; Schema: public; Owner: niemijus
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (id);


--
-- Name: ingredients ingredients_pkey; Type: CONSTRAINT; Schema: public; Owner: niemijus
--

ALTER TABLE ONLY public.ingredients
    ADD CONSTRAINT ingredients_pkey PRIMARY KEY (id);


--
-- Name: recipes_ingredients recipes_ingredients_pkey; Type: CONSTRAINT; Schema: public; Owner: niemijus
--

ALTER TABLE ONLY public.recipes_ingredients
    ADD CONSTRAINT recipes_ingredients_pkey PRIMARY KEY (id);


--
-- Name: recipes recipes_pkey; Type: CONSTRAINT; Schema: public; Owner: niemijus
--

ALTER TABLE ONLY public.recipes
    ADD CONSTRAINT recipes_pkey PRIMARY KEY (id);


--
-- Name: users unique_username; Type: CONSTRAINT; Schema: public; Owner: niemijus
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT unique_username UNIQUE (username);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: niemijus
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users_recipes users_recipes_pkey; Type: CONSTRAINT; Schema: public; Owner: niemijus
--

ALTER TABLE ONLY public.users_recipes
    ADD CONSTRAINT users_recipes_pkey PRIMARY KEY (id);


--
-- Name: comments comments_recipe_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: niemijus
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_recipe_id_fkey FOREIGN KEY (recipe_id) REFERENCES public.recipes(id);


--
-- Name: recipes_ingredients recipes_ingredients_recipe_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: niemijus
--

ALTER TABLE ONLY public.recipes_ingredients
    ADD CONSTRAINT recipes_ingredients_recipe_id_fkey FOREIGN KEY (recipe_id) REFERENCES public.recipes(id);


--
-- PostgreSQL database dump complete
--

