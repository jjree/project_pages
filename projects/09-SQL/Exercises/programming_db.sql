
-- drop table if exists
drop table if exists programming_language;

-- craete new programming_languages table
create table programming_language (
	id serial primary key, 
	language varchar(20) not null,
	rating int
);

insert into programming_language(language, rating)
values ('HTML', 95),
		('JS', 99),
		('JQuery', 98),
		('MySQL', 70), 
		('MySQL', 70);
		
select * from programming_language;

select * from programming_language
where language='MySQL';

delete from programming_language
where id = 5;
select * from programming_language;

insert into programming_language (language, rating)
values ('Python', 23),
		('C++', 25)
		
update progrmaming_languages