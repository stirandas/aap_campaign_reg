-- =====================================================
-- ANDHRA PRADESH COMPLETE MANDALS DATA
-- Total: 679 mandals across 26 districts
-- Source: Wikipedia (List of mandals of Andhra Pradesh)
-- =====================================================

-- First, clear existing test mandals (keep districts)
DELETE FROM mandals WHERE district_id IN (SELECT district_id FROM districts WHERE state_id = 1);

-- =====================================================
-- ALLURI SITHARAMA RAJU DISTRICT (district_id = 14)
-- =====================================================
INSERT INTO mandals (mandal_name, district_id) VALUES
('Chintapalle', 14),
('Chintur', 14),
('Etapaka', 14),
('Kunavaram', 14),
('Vararamachandrapuram', 14),
('Ananthagiri', 14),
('Araku Valley', 14),
('Dumbriguda', 14),
('G. Madugula', 14),
('Gudem Kotha Veedhi', 14),
('Hukumpeta', 14),
('Koyyuru', 14),
('Paderu', 14),
('Peda Bayalu', 14),
('Addateegala', 14),
('Devipatnam', 14),
('Gangavaram', 14),
('Maredumilli', 14),
('Munchingi Puttu', 14),
('Rajavommangi', 14),
('Rampachodavaram', 14),
('Y. Ramavaram', 14);

-- =====================================================
-- ANAKAPALLI DISTRICT (district_id = 15)
-- =====================================================
INSERT INTO mandals (mandal_name, district_id) VALUES
('Anakapalle', 15),
('Atchutapuram', 15),
('Butchayyapeta', 15),
('Chodavaram', 15),
('Devarapalli', 15),
('Elamanchili', 15),
('K.Kotapadu', 15),
('Kasimkota', 15),
('Munagapaka', 15),
('Paravada', 15),
('Rambilli', 15),
('Sabbavaram', 15),
('Cheedikada', 15),
('Golugonda', 15),
('Kotauratla', 15),
('Madugula', 15),
('Makavarapalem', 15),
('Nakkapalle', 15),
('Narsipatnam', 15),
('Nathavaram', 15),
('Payakaraopeta', 15),
('Ravikamatham', 15),
('Rolugunta', 15),
('Sarvasiddhi Rayavaram', 15);

-- =====================================================
-- ANANTAPURAM DISTRICT (district_id = 1)
-- =====================================================
DELETE FROM mandals WHERE district_id = 1; -- Clear existing samples
INSERT INTO mandals (mandal_name, district_id) VALUES
('Anantapur', 1),
('Atmakur', 1),
('Bukkaraya Samudram', 1),
('Garladinne', 1),
('Kudair', 1),
('Narpala', 1),
('Peddapappur', 1),
('Putlur', 1),
('Raptadu', 1),
('Singanamala', 1),
('Tadipatri', 1),
('Yellanur', 1),
('Gooty', 1),
('Guntakal', 1),
('Pamidi', 1),
('Peddavadugur', 1),
('Uravakonda', 1),
('Vajrakarur', 1),
('Vidapanakal', 1),
('Yadiki', 1),
('Beluguppa', 1),
('Bommanahal', 1),
('Brahmasamudram', 1),
('D.Hirehal', 1),
('Gummagatta', 1),
('Kalyandurg', 1),
('Kambadur', 1),
('Kanekal', 1),
('Kundurpi', 1),
('Rayadurg', 1),
('Settur', 1);

-- =====================================================
-- ANNAMAYYA DISTRICT (district_id = 16)
-- =====================================================
INSERT INTO mandals (mandal_name, district_id) VALUES
('B. Kothakota', 16),
('Kalikiri', 16),
('Kurabalakota', 16),
('Madanapalle', 16),
('Mulakalacheruvu', 16),
('Nimmanapalle', 16),
('Peddathippasamudram', 16),
('Peddamandyam', 16),
('Ramasamudram', 16),
('Thamballapalle', 16),
('Valmikipuram', 16),
('Punganur', 16),
('Sodam', 16),
('Somala', 16),
('Pulicherla', 16),
('Rompicherla', 16),
('Chowdepalle', 16),
('Chitvel', 16),
('Kodur', 16),
('Nandalur', 16),
('Obulavaripalle', 16),
('Penagalur', 16),
('Pullampeta', 16),
('Rajampet', 16),
('T. Sundupalle', 16),
('Veeraballi', 16),
('Chinnamandyam', 16),
('Galiveedu', 16),
('Gurramkonda', 16),
('Kalakada', 16),
('K. V. Palle', 16),
('Lakkireddypalli', 16),
('Pileru', 16),
('Ramapuram', 16),
('Rayachoti', 16),
('Sambepalli', 16);

-- =====================================================
-- BAPATLA DISTRICT (district_id = 17)
-- =====================================================
INSERT INTO mandals (mandal_name, district_id) VALUES
('Bapatla', 17),
('Karlapalem', 17),
('Martur', 17),
('Parchur', 17),
('Pittalavanipalem', 17),
('Yeddanapudi', 17),
('Addanki', 17),
('Ballikurava', 17),
('Chinaganjam', 17),
('Chirala', 17),
('Inkollu', 17),
('Janakavarampanguluru', 17),
('Karamchedu', 17),
('Korisapadu', 17),
('Santhamaguluru', 17),
('Vetapalem', 17),
('Amruthalur', 17),
('Bhattiprolu', 17),
('Cherukupalle', 17),
('Kolluru', 17),
('Nagaram', 17),
('Nizampatnam', 17),
('Repalle', 17),
('Tsundur', 17),
('Vemuru', 17);

-- =====================================================
-- CHITTOOR DISTRICT (district_id = 2)
-- =====================================================
DELETE FROM mandals WHERE district_id = 2; -- Clear existing samples
INSERT INTO mandals (mandal_name, district_id) VALUES
('Chittoor', 2),
('Chittoor Urban', 2),
('Gangadhara Nellore', 2),
('Gudipala', 2),
('Irala', 2),
('Penumuru', 2),
('Puthalapattu', 2),
('Sri Rangaraja Puram', 2),
('Thavanampalle', 2),
('Vedurukuppam', 2),
('Yadamarri', 2),
('Kuppam', 2),
('Ramakuppam', 2),
('Santhipuram', 2),
('Gudipalle', 2),
('Nagari', 2),
('Nindra', 2),
('Palasamudram', 2),
('Vijayapuram', 2),
('Karvetinagar', 2),
('Bangarupalem', 2),
('Gangavaram', 2),
('Palamaner', 2),
('Peddapanjani', 2),
('Punganur', 2),
('Venkatagirikota', 2),
('Baireddipalle', 2);

-- =====================================================
-- DR. B.R. AMBEDKAR KONASEEMA DISTRICT (district_id = 18)
-- =====================================================
INSERT INTO mandals (mandal_name, district_id) VALUES
('Allavaram', 18),
('Amalapuram', 18),
('I. Polavaram', 18),
('Katrenikona', 18),
('Malikipuram', 18),
('Mamidikuduru', 18),
('Mummidivaram', 18),
('Razole', 18),
('Sakhinetipalle', 18),
('Uppalaguptam', 18),
('Ainavilli', 18),
('Alamuru', 18),
('Ambajipeta', 18),
('Atreyapuram', 18),
('Kothapeta', 18),
('P. Gannavaram', 18),
('Ravulapalem', 18),
('K. Gangavaram', 18),
('Kapileswarapuram', 18),
('Mandapeta', 18),
('Ramachandrapuram', 18),
('Rayavaram', 18);

-- =====================================================
-- EAST GODAVARI DISTRICT (district_id = 3)
-- =====================================================
DELETE FROM mandals WHERE district_id = 3; -- Clear existing samples
INSERT INTO mandals (mandal_name, district_id) VALUES
('Chagallu', 3),
('Devarapalle', 3),
('Gopalapuram', 3),
('Kovvur', 3),
('Nallajerla', 3),
('Nidadavole', 3),
('Peravali', 3),
('Tallapudi', 3),
('Undrajavaram', 3),
('Anaparthi', 3),
('Biccavolu', 3),
('Gokavaram', 3),
('Kadiam', 3),
('Korukonda', 3),
('Rajahmundry Urban', 3),
('Rajahmundry Rural', 3),
('Rajanagaram', 3),
('Rangampeta', 3),
('Seethanagaram', 3);

-- =====================================================
-- ELURU DISTRICT (district_id = 19)
-- =====================================================
INSERT INTO mandals (mandal_name, district_id) VALUES
('Bhimadole', 19),
('Denduluru', 19),
('Eluru', 19),
('Kaikalur', 19),
('Kalidindi', 19),
('Mandavalli', 19),
('Mudinepalle', 19),
('Nidamarru', 19),
('Pedapadu', 19),
('Pedavegi', 19),
('Unguturu', 19),
('Buttayagudem', 19),
('Dwaraka Tirumala', 19),
('Jangareddygudem', 19),
('Jeelugu Milli', 19),
('Kamavarapukota', 19),
('Koyyalagudem', 19),
('Kukunoor', 19),
('Polavaram', 19),
('T. Narasapuram', 19),
('Velairpadu', 19),
('Agiripalli', 19),
('Chatrai', 19),
('Chintalapudi', 19),
('Lingapalem', 19),
('Musunuru', 19),
('Nuzvid', 19);

-- =====================================================
-- GUNTUR DISTRICT (district_id = 4)
-- =====================================================
DELETE FROM mandals WHERE district_id = 4; -- Clear existing samples
INSERT INTO mandals (mandal_name, district_id) VALUES
('Guntur East', 4),
('Guntur West', 4),
('Medikonduru', 4),
('Pedakakani', 4),
('Pedanandipadu', 4),
('Phirangipuram', 4),
('Prathipadu', 4),
('Tadikonda', 4),
('Thullur', 4),
('Vatticherukuru', 4),
('Chebrolu', 4),
('Duggirala', 4),
('Kakumanu', 4),
('Kollipara', 4),
('Mangalagiri', 4),
('Ponnur', 4),
('Tadepalle', 4),
('Tenali', 4);

-- =====================================================
-- KAKINADA DISTRICT (district_id = 20)
-- =====================================================
INSERT INTO mandals (mandal_name, district_id) VALUES
('Gollaprolu', 20),
('Kajuluru', 20),
('Kakinada Rural', 20),
('Kakinada Urban', 20),
('Karapa', 20),
('Kothapalle', 20),
('Pedapudi', 20),
('Pithapuram', 20),
('Samalkota', 20),
('Thallarevu', 20),
('Gandepalle', 20),
('Jaggampeta', 20),
('Kirlampudi', 20),
('Kotananduru', 20),
('Peddapuram', 20),
('Prathipadu', 20),
('Rowthulapudi', 20),
('Sankhavaram', 20),
('Thondangi', 20),
('Tuni', 20),
('Yeleswaram', 20);

-- =====================================================
-- KRISHNA DISTRICT (district_id = 5)
-- =====================================================
DELETE FROM mandals WHERE district_id = 5; -- Clear existing samples
INSERT INTO mandals (mandal_name, district_id) VALUES
('Bapulapadu', 5),
('Gannavaram', 5),
('Gudivada', 5),
('Gudlavalleru', 5),
('Nandivada', 5),
('Pedaparupudi', 5),
('Unguturu', 5),
('Avanigadda', 5),
('Bantumilli', 5),
('Challapalli', 5),
('Ghantasala', 5),
('Guduru', 5),
('Koduru', 5),
('Kruthivennu', 5),
('Machilipatnam', 5),
('Mopidevi', 5),
('Nagayalanka', 5),
('Pedana', 5),
('Kankipadu', 5),
('Movva', 5),
('Pamarru', 5),
('Pamidimukkala', 5),
('Penamaluru', 5),
('Thotlavalluru', 5),
('Vuyyuru', 5);

-- =====================================================
-- KURNOOL DISTRICT (district_id = 6)
-- =====================================================
DELETE FROM mandals WHERE district_id = 6; -- Clear existing samples
INSERT INTO mandals (mandal_name, district_id) VALUES
('Adoni', 6),
('Gonegandla', 6),
('Holagunda', 6),
('Kosigi', 6),
('Kowthalam', 6),
('Mantralayam', 6),
('Nandavaram', 6),
('Pedda Kadubur', 6),
('Yemmiganur', 6),
('C.Belagal', 6),
('Gudur', 6),
('Kallur', 6),
('Kodumur', 6),
('Kurnool Urban', 6),
('Kurnool Rural', 6),
('Orvakal', 6),
('Veldurthi', 6),
('Alur', 6),
('Aspari', 6),
('Chippagiri', 6),
('Devanakonda', 6),
('Halaharvi', 6),
('Krishnagiri', 6),
('Maddikera East', 6),
('Pattikonda', 6),
('Tuggali', 6);

-- =====================================================
-- NANDYAL DISTRICT (district_id = 21)
-- =====================================================
INSERT INTO mandals (mandal_name, district_id) VALUES
('Atmakur', 21),
('Bandi Atmakur', 21),
('Jupadu Bungalow', 21),
('Kothapalle', 21),
('Midthuru', 21),
('Nandikotkur', 21),
('Pagidyala', 21),
('Pamulapadu', 21),
('Srisailam', 21),
('Velgodu', 21),
('Banaganapalle', 21),
('Bethamcherla', 21),
('Dhone', 21),
('Koilkuntla', 21),
('Owk', 21),
('Peapally', 21),
('Allagadda', 21),
('Chagalamarri', 21),
('Dornipadu', 21),
('Gadivemula', 21),
('Gospadu', 21),
('Kolimigundla', 21),
('Mahanandi', 21),
('Nandyal Rural', 21),
('Nandyal Urban', 21),
('Panyam', 21),
('Rudravaram', 21),
('Sanjamala', 21),
('Sirivella', 21),
('Uyyalawada', 21);

-- =====================================================
-- NTR DISTRICT (district_id = 22)
-- =====================================================
INSERT INTO mandals (mandal_name, district_id) VALUES
('Chandarlapadu', 22),
('Jaggayyapeta', 22),
('Kanchikacherla', 22),
('Nandigama', 22),
('Penuganchiprolu', 22),
('Vatsavai', 22),
('Veerullapadu', 22),
('A. Konduru', 22),
('Gampalagudem', 22),
('Reddigudem', 22),
('Tiruvuru', 22),
('Vissannapeta', 22),
('G.Konduru', 22),
('Ibrahimpatnam', 22),
('Mylavaram', 22),
('Vijayawada Rural', 22),
('Vijayawada North', 22),
('Vijayawada Central', 22),
('Vijayawada East', 22),
('Vijayawada West', 22);

-- =====================================================
-- PALNADU DISTRICT (district_id = 23)
-- =====================================================
INSERT INTO mandals (mandal_name, district_id) VALUES
('Dachepalle', 23),
('Durgi', 23),
('Gurazala', 23),
('Karempudi', 23),
('Macherla', 23),
('Machavaram', 23),
('Piduguralla', 23),
('Rentachintala', 23),
('Veldurthi', 23),
('Bollapalle', 23),
('Chilakaluripet', 23),
('Edlapadu', 23),
('Ipuru', 23),
('Nadendla', 23),
('Narasaraopet', 23),
('Nuzendla', 23),
('Rompicherla', 23),
('Savalyapuram', 23),
('Vinukonda', 23),
('Amaravathi', 23),
('Atchampet', 23),
('Bellamkonda', 23),
('Krosuru', 23),
('Muppalla', 23),
('Nekarikallu', 23),
('Pedakurapadu', 23),
('Rajupalem', 23),
('Sattenapalle', 23);

-- =====================================================
-- PARVATHIPURAM MANYAM DISTRICT (district_id = 24)
-- =====================================================
INSERT INTO mandals (mandal_name, district_id) VALUES
('Bhamini', 24),
('Gummalakshmipuram', 24),
('Jiyyammavalasa', 24),
('Kurupam', 24),
('Palakonda', 24),
('Seethampeta', 24),
('Veeraghattam', 24),
('Balijipeta', 24),
('Garugubilli', 24),
('Komarada', 24),
('Makkuva', 24),
('Pachipenta', 24),
('Parvathipuram', 24),
('Salur', 24),
('Seethanagaram', 24);

-- =====================================================
-- PRAKASAM DISTRICT (district_id = 7)
-- =====================================================
DELETE FROM mandals WHERE district_id = 7; -- Clear existing samples
INSERT INTO mandals (mandal_name, district_id) VALUES
('Chandra Sekhara Puram', 7),
('Darsi', 7),
('Donakonda', 7),
('Hanumanthuni Padu', 7),
('Kanigiri', 7),
('Konakanamitla', 7),
('Kurichedu', 7),
('Marripudi', 7),
('Pamuru', 7),
('Pedacherlo Palle', 7),
('Podili', 7),
('Ponnaluru', 7),
('Veligandla', 7),
('Ardhaveedu', 7),
('Bestawaripeta', 7),
('Cumbum', 7),
('Dornala', 7),
('Giddalur', 7),
('Komarolu', 7),
('Markapuram', 7),
('Peda Araveedu', 7),
('Pullalacheruvu', 7),
('Racherla', 7),
('Tarlupadu', 7),
('Tripuranthakam', 7),
('Yerragondapalem', 7),
('Chimakurthi', 7),
('Kondapi', 7),
('Kotha Patnam', 7),
('Maddipadu', 7),
('Mundlamuru', 7),
('Naguluppalapadu', 7),
('Ongole', 7),
('Santhanuthala Padu', 7),
('Singarayakonda', 7),
('Tangutur', 7),
('Thallur', 7),
('Zarugumilli', 7);

-- =====================================================
-- SRI POTTI SRI RAMULU NELLORE DISTRICT (district_id = 8)
-- =====================================================
DELETE FROM mandals WHERE district_id = 8; -- Clear existing samples
INSERT INTO mandals (mandal_name, district_id) VALUES
('Ananthasagaram', 8),
('Anumasamudrampeta', 8),
('Atmakur', 8),
('Chejerla', 8),
('Kaluvoya', 8),
('Marripadu', 8),
('Sangam', 8),
('Sitarampuramu', 8),
('Udayagiri', 8),
('Gudluru', 8),
('Kandukur', 8),
('Kondapuram', 8),
('Lingasamudram', 8),
('Ulavapadu', 8),
('Varikuntapadu', 8),
('Voletivaripalem', 8),
('Allur', 8),
('Bogolu', 8),
('Dagadarthi', 8),
('Duttaluru', 8),
('Jaladanki', 8),
('Kaligiri', 8),
('Kavali', 8),
('Kodavaluru', 8),
('Vidavaluru', 8),
('Vinjamuru', 8),
('Buchireddypalem', 8),
('Indukurpet', 8),
('Kovur', 8),
('Manubolu', 8),
('Muttukuru', 8),
('Nellore Urban', 8),
('Nellore Rural', 8),
('Podalakuru', 8),
('Rapuru', 8),
('Saidapuramu', 8),
('Thotapalligudur', 8),
('Venkatachalam', 8);

-- =====================================================
-- SRI SATHYA SAI DISTRICT (district_id = 25)
-- =====================================================
INSERT INTO mandals (mandal_name, district_id) VALUES
('Bathalapalle', 25),
('Chennekothapalle', 25),
('Dharmavaram', 25),
('Kanaganapalle', 25),
('Mudigubba', 25),
('Ramagiri', 25),
('Tadimarri', 25),
('Amadagur', 25),
('Gandlapenta', 25),
('Kadiri', 25),
('Lepakshi', 25),
('Nallacheruvu', 25),
('Nambulapulakunta', 25),
('Tanakal', 25),
('Agali', 25),
('Amarapuram', 25),
('Chilamathur', 25),
('Gudibanda', 25),
('Hindupur', 25),
('Madakasira', 25),
('Parigi', 25),
('Penukonda', 25),
('Roddam', 25),
('Rolla', 25),
('Somandepalle', 25),
('Talupula', 25),
('Bukkapatnam', 25),
('Gorantla', 25),
('Kothacheruvu', 25),
('Nallamada', 25),
('Obuladevaracheruvu', 25),
('Puttaparthi', 25);

-- =====================================================
-- SRIKAKULAM DISTRICT (district_id = 9)
-- =====================================================
DELETE FROM mandals WHERE district_id = 9; -- Clear existing samples
INSERT INTO mandals (mandal_name, district_id) VALUES
('Ichchapuram', 9),
('Kanchili', 9),
('Kaviti', 9),
('Mandasa', 9),
('Nandigam', 9),
('Palasa', 9),
('Sompeta', 9),
('Vajrapukothuru', 9),
('Amadalavalasa', 9),
('Burja', 9),
('Etcherla', 9),
('Ganguvarisigadam', 9),
('Gara', 9),
('Jalumuru', 9),
('Laveru', 9),
('Narasannapeta', 9),
('Polaki', 9),
('Ponduru', 9),
('Ranastalam', 9),
('Sarubujjili', 9),
('Srikakulam', 9),
('Hiramandalam', 9),
('Kotabommali', 9),
('Kothuru', 9),
('Lakshminarsupeta', 9),
('Meliaputti', 9),
('Pathapatnam', 9),
('Santhabommali', 9),
('Saravakota', 9),
('Tekkali', 9);

-- =====================================================
-- TIRUPATI DISTRICT (district_id = 26)
-- =====================================================
INSERT INTO mandals (mandal_name, district_id) VALUES
('Balayapalli', 26),
('Chillakur', 26),
('Chittamur', 26),
('Dakkili', 26),
('Gudur', 26),
('Kota', 26),
('Vakadu', 26),
('Venkatagiri', 26),
('K. V. B. Puram', 26),
('Pellakur', 26),
('Satyavedu', 26),
('Sullurpeta', 26),
('Tada', 26),
('Varadaiahpalem', 26),
('Chandragiri', 26),
('Chinnagottigallu', 26),
('Pakala', 26),
('Pichatur', 26),
('Renigunta', 26),
('Tirupati Rural', 26),
('Tirupati Urban', 26),
('Yerpedu', 26),
('Buchinaidu Khandrika', 26),
('Kalahasti', 26),
('Narayanavanam', 26),
('Palasamudram', 26),
('Ramasamudram', 26),
('Thottambedu', 26),
('Venkatagiri', 26);

-- =====================================================
-- VISAKHAPATNAM DISTRICT (district_id = 10)
-- =====================================================
DELETE FROM mandals WHERE district_id = 10; -- Clear existing samples
INSERT INTO mandals (mandal_name, district_id) VALUES
('Anandapuram', 10),
('Bheemunipatnam', 10),
('Chodavaram', 10),
('Gajuwaka', 10),
('Padmanabham', 10),
('Pedagantyada', 10),
('Pendurthi', 10),
('Visakhapatnam Urban', 10),
('Visakhapatnam Rural', 10);

-- =====================================================
-- VIZIANAGARAM DISTRICT (district_id = 11)
-- =====================================================
DELETE FROM mandals WHERE district_id = 11; -- Clear existing samples
INSERT INTO mandals (mandal_name, district_id) VALUES
('Badangi', 11),
('Bhogapuram', 11),
('Bobbili', 11),
('Bondapalle', 11),
('Cheepurupalle', 11),
('Denkada', 11),
('Gajapathinagaram', 11),
('Gantyada', 11),
('Gurla', 11),
('Jami', 11),
('Kothavalasa', 11),
('Kurupam', 11),
('Lakkavarapukota', 11),
('Merakamudidam', 11),
('Nellimarla', 11),
('Parvathipuram', 11),
('Pusapatirega', 11),
('Ramabhadrapuram', 11),
('Seethanagaram', 11),
('Srungavarapukota', 11),
('Therlam', 11),
('Vepada', 11),
('Vizianagaram Urban', 11),
('Vizianagaram Rural', 11);

-- =====================================================
-- WEST GODAVARI DISTRICT (district_id = 12)
-- =====================================================
DELETE FROM mandals WHERE district_id = 12; -- Clear existing samples
INSERT INTO mandals (mandal_name, district_id) VALUES
('Achanta', 12),
('Akividu', 12),
('Attili', 12),
('Bhimavaram', 12),
('Ganapavaram', 12),
('Iragavaram', 12),
('Kalla', 12),
('Mogalthur', 12),
('Narsapuram', 12),
('Palacole', 12),
('Palacoderu', 12),
('Pentapadu', 12),
('Poduru', 12),
('T. Narasapuram', 12),
('Tadepalligudem', 12),
('Tanuku', 12),
('Undi', 12),
('Veeravasaram', 12),
('Yelamanchili', 12);

-- =====================================================
-- YSR KADAPA DISTRICT (district_id = 13)
-- =====================================================
DELETE FROM mandals WHERE district_id = 13; -- Clear existing samples
INSERT INTO mandals (mandal_name, district_id) VALUES
('Badvel', 13),
('Chakrayapet', 13),
('Gopavaram', 13),
('Kadapa', 13),
('Kadapa Urban', 13),
('Mylavaram', 13),
('Mydukur', 13),
('Penagalur', 13),
('Porumamilla', 13),
('Proddatur', 13),
('Pulivendla', 13),
('Rajupalem', 13),
('Rayachoti', 13),
('Sambepalle', 13),
('Sidhout', 13),
('Simhadripuram', 13),
('T. Sundupalle', 13),
('Vallur', 13),
('Vemula', 13),
('Vempalle', 13),
('Yerraguntla', 13);

-- =====================================================
-- VERIFICATION QUERY
-- =====================================================
-- Count mandals per district
SELECT 
    d.district_name,
    COUNT(m.mandal_id) as mandal_count
FROM districts d
LEFT JOIN mandals m ON d.district_id = m.district_id
WHERE d.state_id = 1
GROUP BY d.district_id, d.district_name
ORDER BY d.district_name;

-- Total mandals
SELECT COUNT(*) as total_mandals FROM mandals 
WHERE district_id IN (SELECT district_id FROM districts WHERE state_id = 1);
