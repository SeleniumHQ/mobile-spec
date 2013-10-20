Mobile JSON Wire Protocol Specification
=======================================

### *DRAFT*

Introduction
------------
This specification is designed to extend the [JSON Wire
Protocol](https://code.google.com/p/selenium/wiki/JsonWireProtocol) (JSONWP),
a W3C working draft for web browser automation. The JSONWP has been greatly
successful for that purpose. The need for automation of native and hybrid
mobile applications can be met by the extension of the JSONWP, which already
has a proven basic automation framework (architecture, interaction model,
etc...).

The initial details of this specification were worked out at a series of
meetings held in Mozilla's offices in London in August of 2013. The
participants were:

* David Burns (Mozilla) - [website]() - [twitter]()
* Dominik Dary (eBay) - [website]() - [twitter]()
* Jonathan Lipps (Sauce Labs) - [website](http://jonathanlipps.com) - [twitter](http://twitter.com/jlipps)
* Jason ? (Facebook) - [website]() - [twitter]()
* François Reynaud (eBay) - [website]() - [twitter]()
* Simon Stewart (Facebook) - [website]() - [twitter]()
* Santiago Suarez Ordoñez (Sauce Labs) - [website]() - [twitter]()

Sessions
--------
Sessions work just like WebDriver: you POST to /session and receive a sessionId
as a response if the server can give you one, at which point you can send
further automation commands. If the server can't start a session, for example
if another session is running and only one session can be handled at a time,
the server must return the appropriate 500 response. Sessions are ended with
a DELETE to /session/:id as per the original WebDriver spec.

The server may but is not required to launch the AUT or a device/simulator in
the process of creating a session. It may but is not required to perform some
kind of cleaning or resetting of the AUT in order to provide a clean test
environment. It may but is not required to stop the running AUT at the session
end. It may but is not required to remove the AUT from the device or otherwise
reset the device state after the session is complete. In general, it is the
responsibility of the user to manage the test environment; it is not a part of
this specification. But a server conforming to this specification may by other
means provide that functionality as a convenience.

Desired Capabilities
--------------------

New desired capability keys:

* `automationName`: specific automation tool, e.g., `appium`, `ios-driver`, `selendroid`
* `platformName`: platform to automate, e.g., `Android`, `iOS`
* `platformVersion`: platform version e.g., `4.3` (for Android) or `6.1` (for iOS)
* `deviceName`: specific device names including version information, e.g., `Nexus 4`, `iPhone 4S`, `iPhone Simulator`, `iPad Mini`
* `app` (optional): path or uri to AUT
* `browserName` (optional): web browser to automate as a webdriver session, e.g., `Safari`, `Chrome`

Locator Strategies
------------------
The following locator strategies must be supported for non-HTML-based platforms:

* `class_name`: a string representing the UI element type for a given platform, e.g., `UIAPickerWheel` for iOS or `android.widget.Button` for Android
    * TODO: decide for iOS whether it should be `UIAPickerWheel` or `UIPickerWheel`
* `accessibility_id`: a string representing the accessibility id or label attached to a given element, e.g., for iOS the accessibility identifier and for Android the content-description
* `xpath`: a valid xpath string applied to the XML document that would be retrieved using the page source command

The following locator strategies may be supported, depending on the automation
platform:

* `id`: a string corresponding to a resource ID
* `android_uiautomator`: a string corresponding to a recursive element search using the UiAutomator library (Android only)
    * TODO: specify this
* `ios_uiautomation`: a string corresponding to a recursive element search using the UIAutomation library (iOS-only)
* TODO: figure out whether server should report support of these strategies

If automating a mobile browser in WebDriver mode, or a platform that uses HTML
as its element hierarchy, the usual array of WebDriver commands must be
supported instead, with their usual semantics.

Page Source
-----------
All platforms must respond to the `GET source` command with an XML (or HTML in
the case of HTML-based platforms) document representing the UI hierarchy. The
precise structure of the document may differ from platform to platform. Schemas
that must be followed for iOS and Android automation are as follows:

TODO: get together schemas for UIAutomation (iOS), Instruments (Android), and
UiAutomator (Android).

The elements in these documents may be augmented with such attributes as, for
example, ids, in order to support internal behaviors.

Touch Gestures
--------------
All platforms must adopt the Multi-Action API pioneered by Mozilla. In some
cases it will not be possible to support the full range of gestures potentially
described by this API on a given platform. In this case, the platform should
degrade as gracefully as possible. In the case where the action cannot be
faithfully performed at all (for example when requesting a multi-touch gesture
on a platform which can only handle single-touch gestures), the server must
respond with a 500.

TODO: think harder about what we should do when it's not possible to complete
a requested action and what the response should be.

TODO: show what the gestures API actually looks like in terms of server
endpoints that must be supported.

Other Device Features
---------------------
Mobile devices have a variety of sensors and input methods. These are automated
as follows:

* The virtual keyboard: ?
* acceleromator: ?
* geolocation: use regular webdriver endpoints
* rotation (different from orientation): ?
* battery level: ?
* network speed: (maybe we don't want to allow access to this)?

TODO: I feel like we never figured this out

WebViews and Other Contexts
---------------------------
One common feature of mobile platforms is the ability to embed a chromeless
webbrowser inside of a 'native' application. These are called 'webviews', and,
if possible, a server for a given platform should implement support for
automating the webview using the full, regular, WebDriver API.

This creates a situation where there are two potential contexts for automation
in a given AUT: the native layer and the webview layer. If providing webview
support, the server must have the following endpoints:

* GET /session/:sessionid/contexts
* POST /session/:sessionid/context

The first endpoint must return a possibly-empty array of strings. Each string
must be the arbitrary name of an available context, e.g., one of possibly
multiple webviews.  The second must interpret the body of the request as the
name of an available context. If that context is not found, a NoSuchContext
error must be returned.  If the context is available, the server must switch
automation to that context, such that all subsequent commands are taken to
apply to that context. If the body of the POST is `null`, the server must
return to the original context.

TODO: look up POST /window to make sure this matches.

If a server receives a request at an endpoint which is valid in some context
but not the currently active context (for example if a user calls
`driver.get()` in a native context instead of a webview context), the server
must respond with an InvalidContentException.

Waiting for Conditions
----------------------
The server must respond to the management commands for implicit wait timeouts,
such that when a user sets an implicit wait timeout and tries to find an
element(s), the server keeps trying to find the element(s) until that timeout
expires, rather than responding with the first failure to find the element(s).

TODO: figure out what the serversidewait implementation will be and talk about
it.
