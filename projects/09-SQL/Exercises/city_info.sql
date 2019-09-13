create table cities (
	city varchar(30) not null, 
	state varchar(30) not null, 
	population int
);

insert into cities (city, state, population)
values ('Alameda', 'California', 79177), 
	('Mesa', 'Arizona', 496401), 
	('Boerne', 'Texas', 16056),
	('Anaheim', 'California', 352497), 
	('Tucson', 'Arizona', 535677), 
	('Garland', 'Texas', 238002);
	

select * from cities;

select city from cities;

select * from cities
where state = 'Arizona';

select * from cities
where population <100000;

select * from cities
where state = 'California' and population <100000;

