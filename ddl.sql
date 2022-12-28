-- DDL
create DATABASE if not exists traveldbms;
use traveldbms;
create table if not exists USER(uid int(6)  primary key not null, password varchar(15) not null);
create table if not exists Userprofile(username varchar(30) not null,Age int , doorNo varchar(7) not null , street varchar(20) not null,pincode int(6),city varchar(15) not null,uid int(6) not null,primary key(username,uid),foreign key(uid) references USER(uid) on delete cascade);
create table if not exists HOTELS(Hotel_id varchar(10) primary key,Hotel_Name varchar(20) not null,city varchar(15) not null,priceperperson int not null);
create table if not exists BUS(Bus_Number varchar(10) primary key,Bus_name varchar(20) not null,src varchar(20) not null,dest varchar(20) not null,priceperperson int not null);
create table if not exists flights(flight_number varchar(10) primary key,flight_name varchar(20) not null,src varchar(20) not null,dest varchar(20) not null,fareperperson int not null);
create table if not exists user_hotel(booking_date date not null,no_of_persons int(2),Hotel_id varchar(10) not null,uid int(6) not null,primary key(Hotel_id,uid,booking_date),foreign key(uid) references USER(uid) on delete cascade,foreign key(Hotel_id) references HOTELS(Hotel_id) on delete cascade);
create table if not exists user_bus(travel_date date not null,no_of_persons int(2),Bus_Number varchar(10)  not null,uid int(6) not null,primary key(Bus_Number,uid,travel_date),foreign key(uid) references USER(uid) on delete cascade,foreign key(Bus_Number) references BUS(Bus_Number) on delete cascade);
create table if not exists user_flight(travel_date date not null,no_of_persons int(2),flight_number varchar(10) not null,uid int(6) not null,primary key(flight_number,uid,travel_date),foreign key(uid) references USER(uid) on delete cascade,foreign key(flight_number) references flights(flight_number) on delete cascade);
create table if not exists UserBookingInfo(Transaction_id int not null AUTO_INCREMENT,TDate date,Amount int not null,ServiceType varchar(10) not null,ServiceId varchar(10) not null,ServiceDate date not null,uid int(6) not null,foreign key(uid) references USER(uid) on delete cascade,primary key(Transaction_id,uid));


-- TRIGGERS and FUNCTIONS
--t1)Update money transaction details into transaction table when user booked a hotel.
Delimiter $
CREATE FUNCTION find_hotelprice(hotelid varchar(20),cnt int)
RETURNS int
DETERMINISTIC
BEGIN
DECLARE RESULT int;
select cnt*priceperperson into RESULT from hotels where hotel_id=hotelid;
return RESULT;
END$
Delimiter ;

Delimiter $
create trigger add_transaction_details after insert on user_hotel
for each row 
Begin
	insert into userbookinginfo(TDate,Amount,ServiceType,ServiceId,ServiceDate,Uid) 
	VALUES(SYSDATE(),find_hotelprice(new.hotel_id,new.no_of_persons),"hotel",new.hotel_id,new.booking_date,new.uid);
End$
Delimiter ;

--t2)Update money transaction details into transaction table when user booked a bus.
Delimiter $
CREATE FUNCTION calculate_busfare(busno varchar(20),cnt int)
RETURNS int
DETERMINISTIC
BEGIN
DECLARE RESULT int;
select cnt*priceperperson into RESULT from bus where bus_number=busno;
return RESULT;
END$
Delimiter ;

Delimiter $
create trigger add_transaction_details_bus after insert on user_bus
for each row 
Begin
	insert into userbookinginfo(TDate,Amount,ServiceType,ServiceId,ServiceDate,Uid) 
	VALUES(SYSDATE(),calculate_busfare(new.bus_number,new.no_of_persons),"bus",new.bus_number,new.travel_date,new.uid);
End$
Delimiter ;

--t3)Update money transaction details into transaction table when user booked a flight.
Delimiter $
CREATE FUNCTION calculate_flightfare(flightno varchar(20),cnt int)
RETURNS int
DETERMINISTIC
BEGIN
DECLARE RESULT int;
select cnt*fareperperson into RESULT from flights where flight_number=flightno;
return RESULT;
END$
Delimiter ;

Delimiter $
create trigger add_transaction_details_flights after insert on user_flight
for each row 
Begin
	insert into userbookinginfo(TDate,Amount,ServiceType,ServiceId,ServiceDate,Uid) 
	VALUES(SYSDATE(),calculate_flightfare(new.flight_number,new.no_of_persons),"flight",new.flight_number,new.travel_date,new.uid);
End$
Delimiter ;


-- VIEWS
--v1) View for showing user and flight details together.
CREATE VIEW flightusers AS
select up.uid,up.username,uf.no_of_persons,f.flight_name,f.flight_number,f.fareperperson*uf.no_of_persons as totalcost,uf.travel_date 
from userprofile as up join user_flight as uf on up.uid=uf.uid join flights as f on f.flight_number=uf.flight_number;
