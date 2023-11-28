use todoapp;

drop table if exists users;
drop table if exists todos;

create table users (
	id int(10) not null auto_increment,
    email varchar(100) default null,
    username varchar(50) default null,
    first_name varchar(40) default null,
    last_name varchar(40) default null,
    hashed_password varchar(200) default null,
    is_active int(1) default null,
    primary key (id)
    ) engine = InnoDB Auto_increment =1 default charset= latin1;
    
    
create table todos (
	id int(10) not null auto_increment,
    title varchar(200) default null,
    description varchar(200) default null,
    priority int(1) default null,
    complete int(1) default null,
    owner_id int(10) default null,
    primary key (id),
    foreign key (owner_id) references users(id)
    ) engine = InnoDB Auto_increment =1 default charset= latin1;
    
    