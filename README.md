#researchDevAO - RTP 

###Curent Version - v1.4.1
A proof of concept for the research being done at The Ohio State University by Agustin Ortiz advised by Rajiv Ramnanth
##Real Time Presentation API
The purpose of the software tool is to allow a user to pull up the most relevant piece of document data based on surrounding conversation data happening at a given moment. This gives users an opportunity to store web pages as document data, and retrieve those web pages based on some text interpreted as a conversation. The relevance of the document retrieval methods are being researched, validated, and tested by Agustin Ortiz.

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


