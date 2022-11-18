CREATE TABLE "public.country_temperature_evolution" (
	"temperature_id" integer,
	"country" varchar(35) NOT NULL,
	"year" integer NOT NULL,
	"month" integer NOT NULL,
	"average_temperature" FLOAT NOT NULL,
	"average_temperature_uncertainty" FLOAT NOT NULL,
	CONSTRAINT "country_temperature_evolution_pk" PRIMARY KEY ("temperature_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.demographic" (
	"state_code" TEXT(2) NOT NULL,
	"total_population" integer NOT NULL,
	"male_population" integer NOT NULL,
	"female_population" integer NOT NULL,
	"number_of_veterans" integer NOT NULL,
	"foregin_born" integer NOT NULL,
	"median_age" FLOAT NOT NULL,
	"average_household_size" FLOAT NOT NULL,
	CONSTRAINT "demographic_pk" PRIMARY KEY ("state_code")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.world_airports" (
	"airport_id" varchar(7) NOT NULL,
	"airport_name" varchar(100) NOT NULL,
	"airport_type" varchar(6) NOT NULL,
	"iata_code" varchar(4),
	"municipality_code" varchar(8),
	"municipality" varchar(65),
	"region_code" varchar(5),
	"region" varchar(25),
	"country_code" TEXT(2),
	"country" varchar(35),
	"continent_code" TEXT(2),
	"continent" varchar(13),
	"elevation_ft" FLOAT,
	"latitude" FLOAT,
	"longitude" FLOAT,
	CONSTRAINT "world_airports_pk" PRIMARY KEY ("airport_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.us_states" (
	"state_code" TEXT(2) NOT NULL,
	"state" varchar(20) NOT NULL UNIQUE,
	CONSTRAINT "us_states_pk" PRIMARY KEY ("state_code")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.visa" (
	"visa_id" integer NOT NULL,
	"visa_type" varchar(3),
	"visa_issuer" TEXT(3),
	"visa_category_code" TEXT(1),
	"visa_category" varchar(10),
	CONSTRAINT "visa_pk" PRIMARY KEY ("visa_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.applicant_origin_country" (
	"origin_country_code" TEXT(3) NOT NULL,
	"origin_country" varchar(35) NOT NULL,
	CONSTRAINT "applicant_origin_country_pk" PRIMARY KEY ("origin_country_code")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.status_flag" (
	"status_flag_id" integer NOT NULL,
	"arriaval_flag" TEXT(1),
	"departure_flag" TEXT(1),
	"update_flag" TEXT(1),
	"match_flag" TEXT(1),
	CONSTRAINT "status_flag_pk" PRIMARY KEY ("status_flag_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.admission_port" (
	"admission_port_code" TEXT(3) NOT NULL,
	"admission_port" varchar(43) NOT NULL,
	CONSTRAINT "admission_port_pk" PRIMARY KEY ("admission_port_code")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.arriaval_mode" (
	"arriaval_mode_id" integer NOT NULL,
	"mode_code" TEXT(1),
	"airline" varchar(5),
	"flight_number" varchar(10),
	"mode" varchar(15),
	CONSTRAINT "arriaval_mode_pk" PRIMARY KEY ("arriaval_mode_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.date" (
	"date" DATE NOT NULL,
	"year" integer NOT NULL,
	"quarter" integer NOT NULL,
	"month" integer NOT NULL,
	"week_of_year" integer NOT NULL,
	"day_of_week" integer NOT NULL,
	"day_of_month" integer NOT NULL,
	"day_of_year" integer NOT NULL,
	CONSTRAINT "date_pk" PRIMARY KEY ("date")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.immigrant_application" (
	"file_id" integer NOT NULL,
	"ins_number" integer,
	"admission_number" integer,
	"applicant_age" integer,
	"applicant_birth_year" integer,
	"gender" TEXT(1),
	"occupation" TEXT(3),
	"visa_id" integer,
	"application_date" DATE,
	"admission_port_code" TEXT(3),
	"arriaval_state_code" TEXT(2),
	"arriaval_mode_id" integer,
	"arriaval_date" DATE,
	"departure_date" DATE,
	"limit_date" DATE,
	"status_flag_id" integer,
	"birth_country" TEXT(3),
	"residence_country" TEXT(3),
	CONSTRAINT "immigrant_application_pk" PRIMARY KEY ("file_id")
) WITH (
  OIDS=FALSE
);













ALTER TABLE "immigrant_application" ADD CONSTRAINT "immigrant_application_fk0" FOREIGN KEY ("visa_id") REFERENCES "visa"("visa_id");
ALTER TABLE "immigrant_application" ADD CONSTRAINT "immigrant_application_fk1" FOREIGN KEY ("admission_port_code") REFERENCES "admission_port"("admission_port_code");
ALTER TABLE "immigrant_application" ADD CONSTRAINT "immigrant_application_fk2" FOREIGN KEY ("arriaval_state_code") REFERENCES "us_states"("state_code");
ALTER TABLE "immigrant_application" ADD CONSTRAINT "immigrant_application_fk3" FOREIGN KEY ("arriaval_mode_id") REFERENCES "arriaval_mode"("arriaval_mode_id");
ALTER TABLE "immigrant_application" ADD CONSTRAINT "immigrant_application_fk4" FOREIGN KEY ("arriaval_date") REFERENCES "date"("date");
ALTER TABLE "immigrant_application" ADD CONSTRAINT "immigrant_application_fk5" FOREIGN KEY ("departure_date") REFERENCES "date"("date");
ALTER TABLE "immigrant_application" ADD CONSTRAINT "immigrant_application_fk6" FOREIGN KEY ("limit_date") REFERENCES "date"("date");
ALTER TABLE "immigrant_application" ADD CONSTRAINT "immigrant_application_fk7" FOREIGN KEY ("status_flag_id") REFERENCES "status_flag"("status_flag_id");
ALTER TABLE "immigrant_application" ADD CONSTRAINT "immigrant_application_fk8" FOREIGN KEY ("birth_country") REFERENCES "applicant_origin_country"("origin_country_code");
ALTER TABLE "immigrant_application" ADD CONSTRAINT "immigrant_application_fk9" FOREIGN KEY ("residence_country") REFERENCES "applicant_origin_country"("origin_country_code");












