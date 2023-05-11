PGDMP             	            {           jalon1    15.2    15.2                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    32863    jalon1    DATABASE     y   CREATE DATABASE jalon1 WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'French_France.1252';
    DROP DATABASE jalon1;
                postgres    false            �            1259    32865    image    TABLE     l   CREATE TABLE public.image (
    id_image integer NOT NULL,
    image_name character varying(20) NOT NULL
);
    DROP TABLE public.image;
       public         heap    postgres    false            �            1259    32864    image_id_image_seq    SEQUENCE     �   CREATE SEQUENCE public.image_id_image_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.image_id_image_seq;
       public          postgres    false    215                       0    0    image_id_image_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.image_id_image_seq OWNED BY public.image.id_image;
          public          postgres    false    214            �            1259    32872    list_of_step    TABLE     �  CREATE TABLE public.list_of_step (
    id_list_of_step integer NOT NULL,
    id_image smallint NOT NULL,
    distance_step double precision NOT NULL,
    angle_step double precision NOT NULL,
    index_step smallint NOT NULL,
    name_step character varying(20) NOT NULL,
    CONSTRAINT list_of_step_angle_step_check CHECK ((angle_step < (3.14)::double precision)),
    CONSTRAINT list_of_step_angle_step_check1 CHECK ((angle_step >= (0)::double precision)),
    CONSTRAINT list_of_step_distance_step_check CHECK ((distance_step >= (0)::double precision)),
    CONSTRAINT list_of_step_distance_step_check1 CHECK ((distance_step <= (99)::double precision))
);
     DROP TABLE public.list_of_step;
       public         heap    postgres    false            �            1259    32871     list_of_step_id_list_of_step_seq    SEQUENCE     �   CREATE SEQUENCE public.list_of_step_id_list_of_step_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 7   DROP SEQUENCE public.list_of_step_id_list_of_step_seq;
       public          postgres    false    217                       0    0     list_of_step_id_list_of_step_seq    SEQUENCE OWNED BY     e   ALTER SEQUENCE public.list_of_step_id_list_of_step_seq OWNED BY public.list_of_step.id_list_of_step;
          public          postgres    false    216            j           2604    32868    image id_image    DEFAULT     p   ALTER TABLE ONLY public.image ALTER COLUMN id_image SET DEFAULT nextval('public.image_id_image_seq'::regclass);
 =   ALTER TABLE public.image ALTER COLUMN id_image DROP DEFAULT;
       public          postgres    false    214    215    215            k           2604    32875    list_of_step id_list_of_step    DEFAULT     �   ALTER TABLE ONLY public.list_of_step ALTER COLUMN id_list_of_step SET DEFAULT nextval('public.list_of_step_id_list_of_step_seq'::regclass);
 K   ALTER TABLE public.list_of_step ALTER COLUMN id_list_of_step DROP DEFAULT;
       public          postgres    false    216    217    217                      0    32865    image 
   TABLE DATA           5   COPY public.image (id_image, image_name) FROM stdin;
    public          postgres    false    215   �                 0    32872    list_of_step 
   TABLE DATA           s   COPY public.list_of_step (id_list_of_step, id_image, distance_step, angle_step, index_step, name_step) FROM stdin;
    public          postgres    false    217   j                  0    0    image_id_image_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.image_id_image_seq', 12, true);
          public          postgres    false    214                       0    0     list_of_step_id_list_of_step_seq    SEQUENCE SET     O   SELECT pg_catalog.setval('public.list_of_step_id_list_of_step_seq', 39, true);
          public          postgres    false    216            q           2606    32870    image image_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.image
    ADD CONSTRAINT image_pkey PRIMARY KEY (id_image);
 :   ALTER TABLE ONLY public.image DROP CONSTRAINT image_pkey;
       public            postgres    false    215            s           2606    32881    list_of_step list_of_step_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public.list_of_step
    ADD CONSTRAINT list_of_step_pkey PRIMARY KEY (id_list_of_step);
 H   ALTER TABLE ONLY public.list_of_step DROP CONSTRAINT list_of_step_pkey;
       public            postgres    false    217            u           2606    32883    list_of_step uc_list_of_step 
   CONSTRAINT     g   ALTER TABLE ONLY public.list_of_step
    ADD CONSTRAINT uc_list_of_step UNIQUE (index_step, id_image);
 F   ALTER TABLE ONLY public.list_of_step DROP CONSTRAINT uc_list_of_step;
       public            postgres    false    217    217            v           2606    32884     list_of_step fk_list_of_step_mgr    FK CONSTRAINT     �   ALTER TABLE ONLY public.list_of_step
    ADD CONSTRAINT fk_list_of_step_mgr FOREIGN KEY (id_image) REFERENCES public.image(id_image);
 J   ALTER TABLE ONLY public.list_of_step DROP CONSTRAINT fk_list_of_step_mgr;
       public          postgres    false    215    3185    217               w   x�e��	�@DϚ*\A�:�^rZ�,�uJQ�#�y�/k|f���5J��2�\#��D�\�8����͕��p�n�1�uu��m/�l���ⱗ�H�.�"%v�}�Fr��j�~ ,z3G         �   x�E�K!е9̈$|&w�w���	0�
�K �V�8�E���R��yi߁��ec�3蘻2O�]y�	ߕ7�!�������JZRȖ����ovL6Ғ�l�Qvg�ؽ��t���~�R��
1l     