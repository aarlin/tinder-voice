Tinder Voice
=========================================

Tinder with Voice Commands

![](./images/108.png) ![](./images/plus-108.png) ![](./images/108-alexa.png)

Setup
-----

Download Amazon Alexa from Apple Store or Google Play.

[![iOS](./images/appstore.png)](https://apps.apple.com/us/app/amazon-alexa/id944011620)
[![Android](./images/playstore.png)](https://play.google.com/store/apps/details?id=com.amazon.dee.app&hl=en_US)

To run this example skill you need to do two things. The first is to
deploy the example code in lambda, and the second is to configure the
Alexa skill to use Lambda.

[![Get Started](https://camo.githubusercontent.com/db9b9ce26327ad3bac57ec4daf0961a382d75790/68747470733a2f2f6d2e6d656469612d616d617a6f6e2e636f6d2f696d616765732f472f30312f6d6f62696c652d617070732f6465782f616c6578612f616c6578612d736b696c6c732d6b69742f7475746f7269616c732f67656e6572616c2f627574746f6e732f627574746f6e5f6765745f737461727465642e5f5454485f2e706e67)](./instructions/1-voice-user-interface.md)

Commands
--------------------

You can take a look at the [models/en-US.json](https://github.com/aarlin/tinder-voice/blob/master/models/en-US.json) for the full list of intents.  
Here is a concise table of all the commands.  

| Command                                                | Description                                                  |
|--------------------------------------------------------|--------------------------------------------------------------|
| get profiles                                           | Get a list of recommended users                              |
| swipe left                                             | Pass the current user displayed                              |
| swipe right                                            | Like the current user displayed                              |
| who liked me                                           | See a non-blurred image of who liked you and your like count |
| super like                                             | Super like the current user displayed                        |
| rewind                                                 | Go back to a previous user after swiping left or right       |
| set my location to {City} set my location to {Country} | Set your location to a city or country                       |

Additional Resources
--------------------

### Documentation

-  [Official Alexa Skills Kit Python SDK](https://pypi.org/project/ask-sdk/)
-  [Official Alexa Skills Kit Python SDK Docs](https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/)
-  [Official Alexa Skills Kit Docs](https://developer.amazon.com/docs/ask-overviews/build-skills-with-the-alexa-skills-kit.html)