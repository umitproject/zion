CREATE TABLE software(
-- Attributes --
pk integer,
fk_vendor integer,
fk_type integer,
fk_name integer,
fk_note integer,
description text,
added datetime,
updated datetime);

CREATE TABLE fingerprint(
-- Attributes --
pk integer,
fk_sig1 integer,
fk_raw1 integer,
added datetime,
updated datetime,
fk_software integer);

CREATE TABLE s_attractor(
-- Attributes --
pk interger,
samples integer,
fp blob,
description text);

CREATE TABLE r_tcpisn(
-- Attributes --
pk integer,
samples integer,
series blob,
description text);

CREATE TABLE vendor(
-- Attributes --
pk integer,
name text,
description text);

CREATE TABLE type(
-- Attributes --
pk integer,
name text,
description text);

CREATE TABLE name(
-- Attributes --
pk integer,
name text,
version text,
description text);

CREATE TABLE note(
-- Attributes --
pk integer,
note text,
keywords text);



-- ALTER TABLE note ADD
--     CONSTRAINT  FK_note_software  FOREIGN KEY(unnamed) REFERENCES software (unnamed);


-- ALTER TABLE type ADD
--     CONSTRAINT  FK_type_software  FOREIGN KEY(unnamed) REFERENCES software (unnamed);


-- ALTER TABLE s_attractor ADD
--     CONSTRAINT  FK_s_attractor_fingerprint  FOREIGN KEY(unnamed) REFERENCES fingerprint (unnamed);


-- ALTER TABLE r_tcpisn ADD
--     CONSTRAINT  FK_r_tcpisn_fingerprint  FOREIGN KEY(unnamed) REFERENCES fingerprint (unnamed);


-- ALTER TABLE software ADD
--     CONSTRAINT  FK_software_fingerprint  FOREIGN KEY(unnamed) REFERENCES fingerprint (unnamed);


-- ALTER TABLE software ADD
--     CONSTRAINT  FK_software_vendor  FOREIGN KEY(unnamed) REFERENCES vendor (unnamed);


-- ALTER TABLE software ADD
--     CONSTRAINT  FK_software_name  FOREIGN KEY(unnamed) REFERENCES name (unnamed);
