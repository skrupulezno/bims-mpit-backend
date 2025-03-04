PGDMP      1                }            corporate_portal    15.12    17.2 Q    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            �           1262    16384    corporate_portal    DATABASE     {   CREATE DATABASE corporate_portal WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';
     DROP DATABASE corporate_portal;
                     portal_user    false            �            1259    16501 
   audit_logs    TABLE     �   CREATE TABLE public.audit_logs (
    id integer NOT NULL,
    user_id integer,
    action character varying,
    "timestamp" timestamp without time zone,
    details character varying
);
    DROP TABLE public.audit_logs;
       public         heap r       portal_user    false            �            1259    16500    audit_logs_id_seq    SEQUENCE     �   CREATE SEQUENCE public.audit_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.audit_logs_id_seq;
       public               portal_user    false    229            �           0    0    audit_logs_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.audit_logs_id_seq OWNED BY public.audit_logs.id;
          public               portal_user    false    228            �            1259    16401    departments    TABLE     |   CREATE TABLE public.departments (
    id integer NOT NULL,
    name character varying,
    description character varying
);
    DROP TABLE public.departments;
       public         heap r       portal_user    false            �            1259    16400    departments_id_seq    SEQUENCE     �   CREATE SEQUENCE public.departments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.departments_id_seq;
       public               portal_user    false    217            �           0    0    departments_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.departments_id_seq OWNED BY public.departments.id;
          public               portal_user    false    216            �            1259    16471 	   documents    TABLE       CREATE TABLE public.documents (
    id integer NOT NULL,
    title character varying,
    file_path character varying,
    doc_type character varying,
    description character varying,
    uploaded_at timestamp without time zone,
    uploaded_by integer
);
    DROP TABLE public.documents;
       public         heap r       portal_user    false            �            1259    16470    documents_id_seq    SEQUENCE     �   CREATE SEQUENCE public.documents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.documents_id_seq;
       public               portal_user    false    225            �           0    0    documents_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.documents_id_seq OWNED BY public.documents.id;
          public               portal_user    false    224            �            1259    16428    employee_profiles    TABLE       CREATE TABLE public.employee_profiles (
    id integer NOT NULL,
    user_id integer,
    business_role character varying,
    corporate_email character varying,
    photo_url character varying,
    additional_info character varying,
    department_id integer
);
 %   DROP TABLE public.employee_profiles;
       public         heap r       portal_user    false            �            1259    16427    employee_profiles_id_seq    SEQUENCE     �   CREATE SEQUENCE public.employee_profiles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.employee_profiles_id_seq;
       public               portal_user    false    221            �           0    0    employee_profiles_id_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.employee_profiles_id_seq OWNED BY public.employee_profiles.id;
          public               portal_user    false    220            �            1259    16451    news    TABLE     )  CREATE TABLE public.news (
    id integer NOT NULL,
    title character varying,
    content text,
    news_type character varying,
    is_approved boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    author_id integer,
    department_id integer
);
    DROP TABLE public.news;
       public         heap r       portal_user    false            �            1259    16450    news_id_seq    SEQUENCE     �   CREATE SEQUENCE public.news_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 "   DROP SEQUENCE public.news_id_seq;
       public               portal_user    false    223            �           0    0    news_id_seq    SEQUENCE OWNED BY     ;   ALTER SEQUENCE public.news_id_seq OWNED BY public.news.id;
          public               portal_user    false    222            �            1259    16486    notifications    TABLE     �   CREATE TABLE public.notifications (
    id integer NOT NULL,
    user_id integer,
    message character varying,
    is_read boolean,
    created_at timestamp without time zone
);
 !   DROP TABLE public.notifications;
       public         heap r       portal_user    false            �            1259    16485    notifications_id_seq    SEQUENCE     �   CREATE SEQUENCE public.notifications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.notifications_id_seq;
       public               portal_user    false    227            �           0    0    notifications_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.notifications_id_seq OWNED BY public.notifications.id;
          public               portal_user    false    226            �            1259    16412    sessions    TABLE     �   CREATE TABLE public.sessions (
    id integer NOT NULL,
    user_id integer,
    refresh_token character varying,
    created_at timestamp without time zone,
    expires_at timestamp without time zone
);
    DROP TABLE public.sessions;
       public         heap r       portal_user    false            �            1259    16411    sessions_id_seq    SEQUENCE     �   CREATE SEQUENCE public.sessions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.sessions_id_seq;
       public               portal_user    false    219            �           0    0    sessions_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.sessions_id_seq OWNED BY public.sessions.id;
          public               portal_user    false    218            �            1259    16390    users    TABLE       CREATE TABLE public.users (
    id integer NOT NULL,
    phone_number character varying,
    first_name character varying,
    last_name character varying,
    hashed_password character varying,
    system_role character varying,
    pepper character varying
);
    DROP TABLE public.users;
       public         heap r       portal_user    false            �            1259    16389    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public               portal_user    false    215            �           0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public               portal_user    false    214            �           2604    16504    audit_logs id    DEFAULT     n   ALTER TABLE ONLY public.audit_logs ALTER COLUMN id SET DEFAULT nextval('public.audit_logs_id_seq'::regclass);
 <   ALTER TABLE public.audit_logs ALTER COLUMN id DROP DEFAULT;
       public               portal_user    false    229    228    229            �           2604    16404    departments id    DEFAULT     p   ALTER TABLE ONLY public.departments ALTER COLUMN id SET DEFAULT nextval('public.departments_id_seq'::regclass);
 =   ALTER TABLE public.departments ALTER COLUMN id DROP DEFAULT;
       public               portal_user    false    217    216    217            �           2604    16474    documents id    DEFAULT     l   ALTER TABLE ONLY public.documents ALTER COLUMN id SET DEFAULT nextval('public.documents_id_seq'::regclass);
 ;   ALTER TABLE public.documents ALTER COLUMN id DROP DEFAULT;
       public               portal_user    false    225    224    225            �           2604    16431    employee_profiles id    DEFAULT     |   ALTER TABLE ONLY public.employee_profiles ALTER COLUMN id SET DEFAULT nextval('public.employee_profiles_id_seq'::regclass);
 C   ALTER TABLE public.employee_profiles ALTER COLUMN id DROP DEFAULT;
       public               portal_user    false    220    221    221            �           2604    16454    news id    DEFAULT     b   ALTER TABLE ONLY public.news ALTER COLUMN id SET DEFAULT nextval('public.news_id_seq'::regclass);
 6   ALTER TABLE public.news ALTER COLUMN id DROP DEFAULT;
       public               portal_user    false    223    222    223            �           2604    16489    notifications id    DEFAULT     t   ALTER TABLE ONLY public.notifications ALTER COLUMN id SET DEFAULT nextval('public.notifications_id_seq'::regclass);
 ?   ALTER TABLE public.notifications ALTER COLUMN id DROP DEFAULT;
       public               portal_user    false    226    227    227            �           2604    16415    sessions id    DEFAULT     j   ALTER TABLE ONLY public.sessions ALTER COLUMN id SET DEFAULT nextval('public.sessions_id_seq'::regclass);
 :   ALTER TABLE public.sessions ALTER COLUMN id DROP DEFAULT;
       public               portal_user    false    218    219    219            �           2604    16393    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public               portal_user    false    215    214    215            �          0    16501 
   audit_logs 
   TABLE DATA           O   COPY public.audit_logs (id, user_id, action, "timestamp", details) FROM stdin;
    public               portal_user    false    229   �_       �          0    16401    departments 
   TABLE DATA           <   COPY public.departments (id, name, description) FROM stdin;
    public               portal_user    false    217   �_       �          0    16471 	   documents 
   TABLE DATA           j   COPY public.documents (id, title, file_path, doc_type, description, uploaded_at, uploaded_by) FROM stdin;
    public               portal_user    false    225   b       �          0    16428    employee_profiles 
   TABLE DATA           �   COPY public.employee_profiles (id, user_id, business_role, corporate_email, photo_url, additional_info, department_id) FROM stdin;
    public               portal_user    false    221   1b       �          0    16451    news 
   TABLE DATA           |   COPY public.news (id, title, content, news_type, is_approved, created_at, updated_at, author_id, department_id) FROM stdin;
    public               portal_user    false    223   e       �          0    16486    notifications 
   TABLE DATA           R   COPY public.notifications (id, user_id, message, is_read, created_at) FROM stdin;
    public               portal_user    false    227   /e       �          0    16412    sessions 
   TABLE DATA           V   COPY public.sessions (id, user_id, refresh_token, created_at, expires_at) FROM stdin;
    public               portal_user    false    219   Le       �          0    16390    users 
   TABLE DATA           n   COPY public.users (id, phone_number, first_name, last_name, hashed_password, system_role, pepper) FROM stdin;
    public               portal_user    false    215   Fh       �           0    0    audit_logs_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.audit_logs_id_seq', 1, false);
          public               portal_user    false    228            �           0    0    departments_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.departments_id_seq', 16, true);
          public               portal_user    false    216            �           0    0    documents_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.documents_id_seq', 1, false);
          public               portal_user    false    224            �           0    0    employee_profiles_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.employee_profiles_id_seq', 33, true);
          public               portal_user    false    220            �           0    0    news_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.news_id_seq', 1, false);
          public               portal_user    false    222            �           0    0    notifications_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.notifications_id_seq', 1, false);
          public               portal_user    false    226            �           0    0    sessions_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.sessions_id_seq', 82, true);
          public               portal_user    false    218            �           0    0    users_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.users_id_seq', 18, true);
          public               portal_user    false    214            �           2606    16508    audit_logs audit_logs_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.audit_logs DROP CONSTRAINT audit_logs_pkey;
       public                 portal_user    false    229            �           2606    16408    departments departments_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.departments DROP CONSTRAINT departments_pkey;
       public                 portal_user    false    217            �           2606    16478    documents documents_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.documents DROP CONSTRAINT documents_pkey;
       public                 portal_user    false    225            �           2606    16435 (   employee_profiles employee_profiles_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.employee_profiles
    ADD CONSTRAINT employee_profiles_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.employee_profiles DROP CONSTRAINT employee_profiles_pkey;
       public                 portal_user    false    221            �           2606    16437 /   employee_profiles employee_profiles_user_id_key 
   CONSTRAINT     m   ALTER TABLE ONLY public.employee_profiles
    ADD CONSTRAINT employee_profiles_user_id_key UNIQUE (user_id);
 Y   ALTER TABLE ONLY public.employee_profiles DROP CONSTRAINT employee_profiles_user_id_key;
       public                 portal_user    false    221            �           2606    16458    news news_pkey 
   CONSTRAINT     L   ALTER TABLE ONLY public.news
    ADD CONSTRAINT news_pkey PRIMARY KEY (id);
 8   ALTER TABLE ONLY public.news DROP CONSTRAINT news_pkey;
       public                 portal_user    false    223            �           2606    16493     notifications notifications_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.notifications DROP CONSTRAINT notifications_pkey;
       public                 portal_user    false    227            �           2606    16419    sessions sessions_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.sessions DROP CONSTRAINT sessions_pkey;
       public                 portal_user    false    219            �           2606    16397    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public                 portal_user    false    215            �           1259    16514    ix_audit_logs_id    INDEX     E   CREATE INDEX ix_audit_logs_id ON public.audit_logs USING btree (id);
 $   DROP INDEX public.ix_audit_logs_id;
       public                 portal_user    false    229            �           1259    16409    ix_departments_id    INDEX     G   CREATE INDEX ix_departments_id ON public.departments USING btree (id);
 %   DROP INDEX public.ix_departments_id;
       public                 portal_user    false    217            �           1259    16410    ix_departments_name    INDEX     R   CREATE UNIQUE INDEX ix_departments_name ON public.departments USING btree (name);
 '   DROP INDEX public.ix_departments_name;
       public                 portal_user    false    217            �           1259    16484    ix_documents_id    INDEX     C   CREATE INDEX ix_documents_id ON public.documents USING btree (id);
 #   DROP INDEX public.ix_documents_id;
       public                 portal_user    false    225            �           1259    16449 $   ix_employee_profiles_corporate_email    INDEX     t   CREATE UNIQUE INDEX ix_employee_profiles_corporate_email ON public.employee_profiles USING btree (corporate_email);
 8   DROP INDEX public.ix_employee_profiles_corporate_email;
       public                 portal_user    false    221            �           1259    16448    ix_employee_profiles_id    INDEX     S   CREATE INDEX ix_employee_profiles_id ON public.employee_profiles USING btree (id);
 +   DROP INDEX public.ix_employee_profiles_id;
       public                 portal_user    false    221            �           1259    16469 
   ix_news_id    INDEX     9   CREATE INDEX ix_news_id ON public.news USING btree (id);
    DROP INDEX public.ix_news_id;
       public                 portal_user    false    223            �           1259    16499    ix_notifications_id    INDEX     K   CREATE INDEX ix_notifications_id ON public.notifications USING btree (id);
 '   DROP INDEX public.ix_notifications_id;
       public                 portal_user    false    227            �           1259    16426    ix_sessions_id    INDEX     A   CREATE INDEX ix_sessions_id ON public.sessions USING btree (id);
 "   DROP INDEX public.ix_sessions_id;
       public                 portal_user    false    219            �           1259    16425    ix_sessions_refresh_token    INDEX     ^   CREATE UNIQUE INDEX ix_sessions_refresh_token ON public.sessions USING btree (refresh_token);
 -   DROP INDEX public.ix_sessions_refresh_token;
       public                 portal_user    false    219            �           1259    16399    ix_users_id    INDEX     ;   CREATE INDEX ix_users_id ON public.users USING btree (id);
    DROP INDEX public.ix_users_id;
       public                 portal_user    false    215            �           1259    16398    ix_users_phone_number    INDEX     V   CREATE UNIQUE INDEX ix_users_phone_number ON public.users USING btree (phone_number);
 )   DROP INDEX public.ix_users_phone_number;
       public                 portal_user    false    215            �           2606    16509 "   audit_logs audit_logs_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
 L   ALTER TABLE ONLY public.audit_logs DROP CONSTRAINT audit_logs_user_id_fkey;
       public               portal_user    false    215    3288    229            �           2606    16479 $   documents documents_uploaded_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_uploaded_by_fkey FOREIGN KEY (uploaded_by) REFERENCES public.users(id);
 N   ALTER TABLE ONLY public.documents DROP CONSTRAINT documents_uploaded_by_fkey;
       public               portal_user    false    215    225    3288            �           2606    16443 6   employee_profiles employee_profiles_department_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.employee_profiles
    ADD CONSTRAINT employee_profiles_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.departments(id);
 `   ALTER TABLE ONLY public.employee_profiles DROP CONSTRAINT employee_profiles_department_id_fkey;
       public               portal_user    false    221    3290    217            �           2606    16438 0   employee_profiles employee_profiles_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.employee_profiles
    ADD CONSTRAINT employee_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
 Z   ALTER TABLE ONLY public.employee_profiles DROP CONSTRAINT employee_profiles_user_id_fkey;
       public               portal_user    false    215    221    3288            �           2606    16459    news news_author_id_fkey    FK CONSTRAINT     y   ALTER TABLE ONLY public.news
    ADD CONSTRAINT news_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.users(id);
 B   ALTER TABLE ONLY public.news DROP CONSTRAINT news_author_id_fkey;
       public               portal_user    false    3288    223    215            �           2606    16464    news news_department_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.news
    ADD CONSTRAINT news_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.departments(id);
 F   ALTER TABLE ONLY public.news DROP CONSTRAINT news_department_id_fkey;
       public               portal_user    false    223    217    3290            �           2606    16494 (   notifications notifications_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
 R   ALTER TABLE ONLY public.notifications DROP CONSTRAINT notifications_user_id_fkey;
       public               portal_user    false    227    215    3288            �           2606    16420    sessions sessions_user_id_fkey    FK CONSTRAINT     }   ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
 H   ALTER TABLE ONLY public.sessions DROP CONSTRAINT sessions_user_id_fkey;
       public               portal_user    false    215    219    3288            �      x������ � �      �     x��T[r�@�^�b��*��?�9�$����#!p��"Ek˒�0s#zz%��)��Z���'?%H��+iu&	^���f��R{n�R�-��:�R�N��C��F��^���
����Kxl�[|�ITP�@��4]z(hqj���qv���w�e���%8y�Z瘬L�	y���t��  �����X�_3�ۦ^S�-�A�=�)F�CХG�.E����@j�nD���r�@K��vJ�9GKQ���.��
L�l�	o�?'��\�^;���112���7�DY���8`�~�������F�,�@L���v�Ԑ��a��)���7N��
p��(-cO��Ɉ�rZ���(!�:[����w�n�T�d�[qj���76<~{ޭ��Ks ��P�u���ݣ��`Y��4ŴӰHX���e����>~�8�K��Y;4��|�})ߴ{�tl�h�ӭ�V_��i-��8�J�'��v����㭲e�G�c�I�����}���;V2T������8˲?�6e�      �      x������ � �      �   �  x��TMO�@=�E�@kC�����S�\��7�9�j8��V�D�UUU�=W2��f�Q߬��T��Ǯg��{o,�#�����m{��J�w�ds���^ӎ�xӜ��R
:��.t��)Mt����+��^������0������UA��]��q��Ғ�ZuP�����aJi����F�T�Cd��J}���&5S�jtEv�0�_f�ǘ��5n��s`�Q��R��Y����%:*������&��
�W ;CҌ��
�)��5���tB�8
 ѕTK���'�V MA�5*q�X���8�N� A��i(���2k=�@�rl�*7^m��KEϋv�O&~����U�?�9�^W�B�����+����U�t��.��	o�O��!䊠�X�tKg�C�����0u�yXn�w)��(���/���T�y�����~�2=��͜��C���{����?��T��,䪠�,��S��p'R4;~���B��:�v~j|�Ϫ��=l�p�1����F��;5�cn�^Mv��f`?��r��A_ҍ��٨���4l�(���`�U'��� yi�㐧Әf��������b���:B��0���*�:�4�WM�����j� l��
��Z��d���ϕ��L6H
@�m�⫖�
���N�<�ո���M����U���G��>��ZW�0�.�~@���]4�!f���߰�l˲~Rn�      �      x������ � �      �      x������ � �      �   �  x���ێ�X���)� ���NQ,PA�$D@�*��:S��;q����_!����rh�c�F�2ӵM�A3�j������کں�.q}Q{Z_��s�?���.�Ql80��n�M����hϋƷ������_��,�8a�w:C�ė����O� ŋ���d��^���i^@��E�_ˈ�sI��f��-B1�I��|�+7���ˠ)P��o����*te��v�n��Et?���	�(JT �����~�Μ��Ry�c����xܹo�-�u�}�f�Z��C����ͫ+t��N���IX0?�}E�y��"��PwɽIr	F�b��q��q�ڍy�U����m써ܡ�
�@��L(G �xq���P/g�StΔ��C]4�)���wƪf�ϦW+�#�:��⦙ͪz�#��x��"��}E}W�����������/g%|���6��<.ˠ��^a��\�i�Wݔw�S[��r:�Q(S��W��!�+	�,=���7�{�W`��9��3���ԫ��ni�_t�d��r��{:�! ��?^ޕ���!�9���s�������k�������Q3�8��\��^��!����0�}F��g�����~�wϻ-\�ZiD�βXYt����N�6li���M�M��|�`K߻�K�����xo�Ǉs9G���2�m��=���V+��'�Ed�t���$B�M��!�3�����1�]��&      �     x����n�@F��ϑR�g<�%R�L	�j*63��Iڀ��aU�$	U���QCK��o�8�K0,��s�� ��j@'tI��+��tN��)�QF��Mi5O�Ы5���f���a|�8����������H�6�p�%��8�V�D����F�M�J�݇������g&V�HƵL�m���|���l��c�#o[���[�ޚ0i����Mw�n�؝Þ+���:�������~��hlh�$�E�j,���N�"|�w���0�3�2�@_hF��2?���a�$���7�&M��WJ�8v���}�̞��'�3:�����Q��cUKc�m}@�\�3��o��s��>ڟn�
�h�|�� Y9�w��+b5���UX��A� �k�������-�Z��NTyB)��� 0(��~���4+��5���*L*�^lK�(�ƖfVg� �/@�.��޶�P�+>ˏ�yk����yw��*�ё��y��8�/�m��     