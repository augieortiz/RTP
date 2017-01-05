#researchDevAO - RTP 


##Current Version Beta - v1.6

Landing page made to look more professional.  All mentions of instances were replaced with presentations to make the application easier to understand for the user.  1 bug fixed in the microphone and stop button.  The SpeechRecognitionAPI javascript code is more functional inside the chrome browser.  This would be our first release, but there is no way for users to create accounts so this version is still in Beta.  Lastly we added the capability onto the landing page to request an account which sends an email to the developer.  This is a quick solution until the developer has more time to make a create account page/section.

##Beta - v1.5.2.2

A proof of concept for the research being done at The Ohio State University by Agustin Ortiz advised by Rajiv Ramnanth
##Real Time Presentation API
The purpose of the software tool is to allow a user to pull up the most relevant piece of document data based on surrounding conversation data happening at a given moment. This gives users an opportunity to store web pages as document data, and retrieve those web pages based on some text interpreted as a conversation. The relevance of the document retrieval methods are being researched, validated, and tested by Agustin Ortiz.

#Beta v1.5.2.2

2 bug fixes & 2 additions dealing with id's on custom document urls.  The urls are no longer used as query strings, rather they are the ObjectID stored in the MongoDB.  Displaying this url provided a few bugs but they have been resolved.  The version number is only on the login page and is now a variable for easier modifications.  We have added the url to the document on the results page for devleoper reference while testing.  Small release but necessary for testing.

#Beta v1.5

###Test Results

Every query ran against the mongoDB will be saved in our mySQL database. Each session will store every query result for testing purposes.  There is a new tab in the nav bar labled "Test Results."  We are still working on an export but the table does display for your convienence with functionality to sort and search results.

Updates made to databases via script.  2 feilds added to mongoDB and entirely new table added to mysql

Other chances included:
* Side by side design on the add page
* New addition to nav bar
* Newly designed presentation iFrame
* Plugin for table sorting and searching
* Newly designed thesis page for more of a document feel


#Beta v1.4.1

One additional featureL: Voice Recognition.  One bug fix on empty instances in an account.  Updated thesis page to reflect google doc status

###Voice Recognition
The voice recognition feature is only available in CHROME.  Unfortunatly the client side solution was much more feasable than sending flac files over to the web server for voice recognition.  This leverages the Speech recognition API and uses js functions to put the voice recognition into the text area form input.  This is currently being tested and is still in Beta.

*Minor bug fix: New accounts with zero added instances do not fail to open the add page aymore.

#Beta v1.3.5.2

Two additional features: Instances & Spider Add.  Multiple Bug fixes, and just one thesis update.

###Instances
Instances are now supported.  You can add & delete instances in which you can add documents to.  The relationship is as follows. Users->Instances->Documents.  Each user can have a set of instances, and each instances can have many documents.  This is important so we can test with different subjects/lectures/websites.

###Spider Add
A crawler was implemented into the add page.  Instead of adding just one page at a time, there is now the capability of adding multiple documents at one time.  The crawler will use the top level domain and also add any links included in that page from that same domain.  For example, www.osu.edu is submitted for a spider add.  The document is parsed for all href tags, then that list is truncated based on link that include osu.edu in them that way the subject is not effected.  This isn't optimized so the feature takes a while depending on the number of links.

###UI Upgrades
Added many new UI changes as features like modal windows & animations on form submissions.

###Bugs
*Receive page doesn't load in fake data on the initial GET request
*Inputs are now buttons for a better UI flow
*The dropdown on the add page was removed due to poor UI/UX
*Links on the table are now working and go to the iFrame in place
*Debug mode is turned off in production.

###Thesis
Minor spelling error updates

#Beta v1.0.1.1

Thesis - Updated with more questions.
Bugs - ??? can't remember


##Beta 1.0 Release Notes
Release . Feature Updates . Bug Fixes . Thesis Updates

###Add/Receive Data
You can any URL to the mongo database as a single document data.  It parses the URL, title, and DOM.  This information is then stored in the database.  The DB is not currently relational.  You can then retrieve this information based on some text entered in on the receive page. 

###Login
Login works with a MySQL backend.  Only two accounts are allowed at this current time.  A new account page will be developed in the future.

###Thesis
This page is purely for documenting the thought process throughout my thesis development. 


