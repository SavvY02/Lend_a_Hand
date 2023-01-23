drop database lendahand;
create database lendahand;
use lendahand;

create table volunteers(
	name varchar(255),
    email varchar(255) primary key,
    password varchar(255),
    phone_number bigint(255),
    location varchar(255)
);

create table organisers(
	name varchar(255),
    organisation_name varchar(255) unique,
    email varchar(255) primary key,
    password varchar(255),
    phone_number bigint(255)
);

create table event(
	email varchar(255),
    title varchar(255),
    description varchar(1000),
    scheduled_datetime datetime,
    report boolean,
    status varchar(255),
    location varchar(255),
    primary key (title),
    foreign key (email) references organisers(email)
    );
drop table event_volunteer_table;
create table event_volunteer_table(
	event_title varchar(255),
    volunteer_email varchar(255),
    rating_by_organiser int default 0,
    organiser varchar(255),
    certificate_status varchar(255) default "Not Provided",
    certificate varchar(255),
    foreign key (event_title) references event(title),
    foreign key (volunteer_email) references volunteers(email)
    );
    
    
create table completed_event_table(
	email varchar(255),
    title varchar(255),
    experience_description varchar(255),
    images varchar(255),
    foreign key (email) references organisers(email),
    foreign key (title) references event(title)
    );
    
insert into organisers values
  ('George Mathew (India)','ISER','info@iser.org.in','12345678',6438261937),
  ('James','Isete','info.iseteconference@gmail.com','12345678',9922113456),
  ('Nagarjunan','IRF','info.irfconference@gmail.com','12345678',7892341230),
  ('KrishnaVeni','Asar','papers.asar@gmail.com','12345678',9900234123),
  ('Ashish','ICISS','ICISS@gmail.com','12345678',7894562354),
  ('Sanju Reddy','ICARCSIT','process.ICARCSIT@gmail.com','12345678',6894562354),
  ('Uthej','Kouru','uthejkaranam@gmail.com','organiser',8897465480);
insert event values("uthejkaranam@gmail.com","Tell a Story!","iVolunteer has connected to many NGOs around India who work with children. We will share these audio stories with them so that they can play it for the children they work with. We would appreciate it ","2022-12-21 12:10:00",false,"upcoming","Mumbai");
insert event values("uthejkaranam@gmail.com","Personal Campaign for Carbon Footprint Awareness","92% of people we surveyed in the last 3 years were not aware of the term personal carbon footprint. Your objective is to discover your carbon footprint.","2022-12-27 12:20:00",false,"upcoming","Delhi");
insert event values("uthejkaranam@gmail.com","Teaching Digital literacy to Students","Purpose: To spark curiosity, nurture creativity and build confidence among economically disadvantaged children and teachersfrom across India , To prepare students of tomorrow's world by teaching digital literacy to student community","2022-03-21 12:30:00",false,"completed","Delhi");
insert event values("uthejkaranam@gmail.com","Join Dance Club","Are you a talented person, would you like to use your talent & help others?  If, YES, this opportunity is for you ","2022-12-08 07:30:00",false,"ongoing","Maharashtra");
insert event values("uthejkaranam@gmail.com","Know Your Emotions","Not many of us are brought up to talk easily and openly about how we feel. Even acknowledging feelings and emotions can be difficult. Talking about feelings may make us feel uncomfortable, vulnerable, ashamed, or weak, or maybe something ","2022-12-08 08:30:00",false,"ongoing","Banglore");
insert event values("uthejkaranam@gmail.com","Sathi Of the Underprivileged","Helping a divyang person get a wheelchair by guiding them through the process of documentation.Help an old person get an eye cataract operation through our NGO Partner","2022-06-21 12:00:00",false,"completed","Goa");

insert event values
	("info@iser.org.in","International Conference on Mathematics","International Conference on Maths, Statistics and Applied Science welcomes experts, and students from the world to discuss trending topics and indulge in high-level discussions.it will help you create networks, meet professionals and present your ideas","2022-05-21 11:30:00",false,"ongoing","Kerala");
insert event values
	("info@iser.org.in","Event Management in Decathlon Sports India","Our team is powered to design, manufacture, and sell products that are technically as superior as they are affordable to all. Our designers and engineers partner with sportspersons across the world adding a new dimension to the design process. This coupled with cutting-edge technology and innovation delivers products that are absolute winners. Our focus on various sports from running to water sports, from racket sports to adventure, from dancing to horse riding - is delivered by our passion brands encouraging our customers to play more.","2022-12-06 11:30:00",false,"ongoing","Bengaluru");
insert event values
	("uthejkaranam@gmail.com","Wildlife conservation","Wildlife conservation refers to the practice of protecting wild species and their habitats in order to maintain healthy wildlife species or populations and to restore, protect or enhance natural ecosystems. Major threats to wildlife include habitat destruction, degradation, fragmentation, overexploitation, poaching, pollution and climate change. The IUCN estimates that 27,000 species of the ones assessed are at risk for extinction. Expanding to all existing species, a 2019 UN report on biodiversity put this estimate even higher at a million species. It is also being acknowledged that an increasing number of ecosystems on Earth containing endangered species are disappearing There are also numerous nongovernmental organizations (NGO's) dedicated to conservation such as the Nature Conservancy, World Wildlife Fund, the Wild Animal Health Fund and Conservation International.","2022-12-06 12:30:00",false,"ongoing","Tirupathi");

insert event values("info.irfconference@gmail.com","International Conference on Internet of Things","The key motive of ICITBDIT – 2019 is to provide a world-class platform for the global participants to share their ideas and experience in person with their peers expected to join from different parts of the world. In addition, this gathering will help the delegates to establish research or business relations as well as to find international linkage for future collaborations in their career path. We hope that ICITBDIT outcome will lead to significant contributions to the knowledge base in these up-to-date scientific fields in scope.","2022-05-21 12:50:00",false,"completed","Hyderabad");
insert event values("info.iseteconference@gmail.com","International Conference on Artificial Intelligence","The aim objective of ICAIMLBDE is to present the latest research and results of scientists related Artificial Intelligence, Machine Learning and Big Data Engineering topics. This conference provides opportunities for the different areas delegates to exchange new ideas and application experiences face to face, to establish business or research relations and to find global partners for future collaboration. We hope that the conference results constituted significant contribution to the knowledge in these up to date scientific field. The organizing committee of conference is pleased to invite prospective authors to submit their original manuscripts to ICAIMLBDE.","2022-04-01 12:50:00",false,"completed","Tirupathi");

insert event values("papers.asar@gmail.com","International Conference On Machine Learning","The ICMBDC conference offers a track of quality R&D s from key experts and provides an opportunity in bringing in the new techniques and horizons that will contribute to Machine learning Big data management Cloud and Computing in the next few years. All submitted papers will be under peer review and accepted papers will be published in the conference proceeding. Both academia and industries are invited to present their papers dealing with state-of-art research and future developments.","2023-04-01 12:50:00",false,"upcoming","Nellore");
insert event values("papers.asar@gmail.com","Conference on Information Systems Security","The International Conference on Information Systems Security (ICISS), held annually in India, is a forum for the dissemination of research results and a place for meeting finer minds on computer security. ICISS 2022, the 18th edition of the conference, will be held at IIT Tirupati in the city of Tirupati from December 16 to 20, 2022. The conference will include a high quality technical papers, a set of visionary/invited papers on important and timely topics from well-known leaders in the field, and a session on the work in progress. Alongside the broader objectives, the ICISS 2022 emphasizes enhancing the cooperation between India and Australia on information security research activity. The conference therefore invites the researchers and security enthusiasts to take advantage of the forum to share and discuss the subject concerns to the topic of computer security.","2022-12-08 08:00:00",false,"ongoing","Delhi");

insert into event values("ICISS@gmail.com","International Conference on Advanced Research","The ICARCSIT conference offers a track of quality R&D s from key experts and provides an opportunity in bringing in the new techniques and horizons that will contribute to Advanced Research in Computer Science and Information Technology in the next few years. All submitted papers will be under peer review and accepted papers will be published in the conference proceeding. Both academia and industries are invited to present their papers dealing with state-of-art research and future developments.","2023-05-06 1:50:00",false,"upcoming","Kanpur");
insert into event values("ICISS@gmail.com","Help for a person with chronic disorders","It was a rather gloomy cloudy day when I had a chance to meet Lakhuna Das. I was in the process of documenting stories and journeys of persons with drug-resistant Tuberculosis (DR-TB) and Lakhuna Das’s journey was one such story. My colleague, Mukesh Yadav, at Innovators In Health had already briefed me about the situation.… Read More »The Reality Of A Person Living With Multiple Chronic Diseases","2024-05-06 1:50:00",false,"upcoming","Kolkata");

insert into event values("info.iseteconference@gmail.com","Bail Pola A gratitude festival for Bulls","India is known all over the world for its rich collection of different cultures. People belonging to different religions, regions, caste and sect celebrate various festivals across the country. The uniqueness of Indian festivals is that it revolves around Lord’s birthdays, traditional rituals, seasonal changes, or agricultural yields. One such festival is called Bail Pola… Read More »Bail Pola: A Gratitude Festival For Bulls","2022-12-12",false,"upcoming","Ranchi");
