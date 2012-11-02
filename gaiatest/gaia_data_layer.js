/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this file,
 * You can obtain one at http://mozilla.org/MPL/2.0/. */

var GaiaDataLayer = {

    sendSms: function(number, message){
        // SMS object
        var sms = navigator.mozSms;

        // Send a message
        request = sms.send(number, message);

        request.onerror = function onerror() {
            console.log('Error sending SMS', request.error.name);
        }

        request.onsuccess = function onsuccess() {
            console.log('Success sending SMS', request);
        }
        return request;
    },

    deleteAllSms: function(id){

        // SMS object
        var sms = navigator.mozSms;

        var msgList = new Array();

        var filter = new MozSmsFilter();
        filter.numbers = [''];

        // Send a message
        request = sms.getMessages(filter, false);

        request.onerror = function onerror() {
            console.log('Error finding SMS', request.error.name);
        }

        request.onsuccess = function onsuccess() {
            console.log('Success finding SMS', request);

            cursor = request.result;

            console.log(cursor);

            if(cursor.message){
                console.log("Deleting message", cursor.message.id)
                deleteReq = sms.delete(cursor.message.id);
                // Now get next message in the list
                cursor.continue();
            }

        }

        //return request;
    }
};

