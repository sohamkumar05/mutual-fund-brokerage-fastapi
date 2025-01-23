CREATE TABLE users
(
    id bigserial NOT NULL,
    name character varying(20),
    email character varying(20),
    password character varying(256),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    CONSTRAINT users_pk PRIMARY KEY (id),
    CONSTRAINT users_email UNIQUE (email)
);

CREATE TABLE portfolio
(
    id bigserial NOT NULL,
    user_id bigint,
    mutual_fund_family character varying(50),
    scheme_code bigint,
    is_delete boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    PRIMARY KEY (id),
    CONSTRAINT users_fk FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);
