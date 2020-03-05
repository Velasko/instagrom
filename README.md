Project for the Software development to the cloud course

This project is an a photo social media, similar to instagram.

The user data to be saved are:  
+ 	 Name  
+	 Nickname  
+	 Password  
+	 E-mail  
+	 Personal photo  
	
The system must allow for the user to do the following operations:  
- 	 create an user;  
-	 Alter user's data;  
-	 Publish photos;  
-	Like/dislike other users photos;  
-	See another user's profile and it's photos (All users can see the information of other users - there is no need to send a friend request or to set a profile public/private)  
-	Search a user based on it's nickname;  
-	List the posted photos in a time interval. For this, the inicial and final data must be provided to the filter.  

Project impositions:   
-	The user information must be saved into a relational database, created by the Amazon RDS service;   
-	The uploaded photos must be saved on S3;  
-	The image's likes must be saved using Amazon Dynamo DB.  

The chosen language for implementation is Python 3.7

Required libraries for the execution:
 - Flask (flask, flask-login)
