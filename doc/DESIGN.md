= Decision trees for creating a Python wrapper class for Taniums SOAP API =

== Path 1 Suds ==
  * Most desirable path for "right now"
  * DOC URL: https://fedorahosted.org/suds/wiki/Documentation
  * Source URL: https://fedorahosted.org/suds/
  * Pros:
    * Has not been updated in 4+ years, so is likely very stable
    * Less dev work up front, can handle SOAP requests and responses in pythonific way without having to construct and parse XML by hand
    * Got a working saved question request and response in about 15 minutes
    * While it is a 3rd party module, it's only one and has no compilation deps (so can be included in wrapper package)
  * Cons:
    * Has not been updated in 4+ years, so may not be the best of breed choice for current day SOAP
    * External module, so will need to include setup instructions or include it in lib directory of wrapper package
    * Will require user to supply WSDL (which is not currently available via URL in current product)

== Path 2 SOAPpy ==
  * Not going this path -- GIT repo readme for SOAPpy says to use suds instead of SOAPpy
  * Source URL: https://github.com/kiorky/SOAPpy

== Path 3 ElementTree ==
  * This path might be something for a later version
  * AKA "roll your own SOAP / XML parser"
  * ElementTree is built into python
  * Pros:
    * Can construct a very well defined structure for handling SOAP requests and responses
    * No external dependencies for third party modules
    * No WSDL file required
  * Cons:
    * Would require much more dev work up front

== Path 4 XML Templating ==
  * This path is not very pythonific, not going this route
  * AKA "roll your own SOAP / XML parser using Python String Templates and BeautifulSoup"
  * Pros:
    * No external dependencies for third party modules
    * No WSDL file required
  * Cons:
    * Not a very pythonific way to handle this scenario
    * Error prone since XML messages being constructed "by hand"

= Notes = 
  * Reference for Tanium's SOAP API: http://kb.tanium.com/SOAP
