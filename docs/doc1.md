

# Table of Contents

[TOC]

# Overview

A workflow simplifies development by allowing the implementer to create and chain discrete tasks without the need to write expansive functions. Both the workflow and its tasks are written using the JSON format. A _workflow_ is a JSON object where each property of the object is the name of a _task_. A _task_ is a JSON object where each property of the object is the name of a task _argument_. 

```
{"taskOne":{"type": "log", "message": "hello world"}, "taskTwo":{"type": "log", "message": "good bye world"}}
```

In the example _workflow_ above, the first properties of the JSON document are two tasks named taskOne and taskTwo. Both tasks are of the _log _type and will print a line to the debug log. However, each task will print a unique message specified by it's message argument _value_.

# Chaining Tasks

Tasks in a workflow can be chained together and processed. The workflow engine starts processing a task chain by specifying the first task it will run. The name of this task is also known as an _entry point_. 

```
{"start":{"type": "log", "message": "getting started", "success": "end"}, "end":{"type": "log", "message": "finishing"}}
```

In the example workflow above, there are two tasks named _start_ and _end_. The task specified by the _start_ name will be processed first since _start_ is the name of a entry point used by the workflow engine. When the _start _task completes successfully by printing its message to the debug log, it will run the _end_ task which will print its message to the debug log. 

## Entry Points

The following task names are reserved as specific workflow entry points.

| Name |  |
|------|--|
| load | Task to run when the workflow is loaded.  
This entry point is run internally. |
| start | Task to run when the workflow is started, after _load_ is completed. |
| state | Task to run on an interval, after _start_ is completed.  
Can be used to check to see if patches are up to date every so often. |
| launch | Task to run when the launch button is clicked. |
| repair | Task to run when the repair button is clicked. |
| uninstall | Task to run when the uninstall button is clicked. |
| update | Task to run when the update button is clicked. |
| unload | Task to run when the workflow is unloaded.  
This entry point frees the workflow and should be the last to run. |
| status | Reserved due to conflicts with argument expansion. |
| args | Reserved due to conflicts with argument expansion. |

## SubTasks

Every task can have a _success_, _failure_, and _complete_ property that specifies what task should be run next based on the result of the current task. Some task types have additional properties that specify tasks to run. The example below which shows how the _stringCompare_ task has an _equalTo_ property that specifies the task to run when the two strings specified are equal to one another.

```
"abCompare":{"type": "stringCompare", "stringOne": "a", "stringTwo": "b", "equalTo": "cdCompare"},"cdCompare":{"type": "stringCompare", "stringOne": "c", "stringTwo": "d", "equalTo": "efCompare"},
```

# Expandable Strings

The workflow engine supports expandable strings which are evaluated at run-time. In addition to the core set of expandable strings, the workflow engine also supports these specific strings that are available in certain instances depending on the location specified for the workflow.

| Name | Type | Description |
|------|------|-------------|
| WorkflowPath | string | Path to the workflow file, if loaded from the filesystem. |
| WorkflowDirectory | string | Directory of the workflow file, if loaded from the filesystem. |
| WorkflowURL | string | URL of the workflow, if loaded from a runWorkflow task. |

## Object Expansion

Also unique to the workflow engine is the ability to target specific objects to handle string expansion. A target object might be the workflow itself or a particular task. The following keywords are supported that allow you to specify which object you wish to handle the expansion.

| Name | Description |
|------|-------------|
| This | Current task object. |
| Parent | Current object's parent. |
| Parent:`TN` | Find the parent object with the specified task name (`TN`). |
| Args | Task's arguments. |
| Status | Task or workflow's status variables. |

### **Examples  
**

| Expandable String | Description |
|-------------------|-------------|
| {this.args.applicationName} | Gets the applicationName argument for the current task. |
| {this.parent.args.applicationName} | Gets the applicationName argument from the current task's parent. |
| {this.parent.parent.args.type} | Gets the type argument from the current task's gradparent. |
| {this.parent.status.downloadSpeed} | Gets the downloadSpeed status property for the current task's parent. |
| {workflow.status.startTime} | Get's the current workflow's startTime status property. |

In the example below, the _download _task downloads a file specified by it's url property. When the download is successful, it will the _launch_ task which will launch the file specified by it's parent task's _outputPath_ status property.

```
{"download":{"type": "download", "outputPath": "{Temp}", "url": "https://myurl/myfilename.exe", "success": "launch"}, "launch":{"type": "launch", "path": "{this.parent.status.outputPath}", "successCode": 0, "waitForExit": true}}
```

# Tasks

_Required arguments are bold in the arguments list._

All tasks cam have the following reserved arguments:

| Name | Type | Description |
|------|------|-------------|
| type | string | Type of task. |
| title | string | Title to show when the task is first started. |
| status | string or string/array | Status to show when task is first started.  
If _array of strings_, then first string is _start_ status and second string is _success_ status.  |
| ignoreError | boolean/array | Ignore error conditions for this task.  
If _true_ ignores all errors, otherwise if _array of strings_ ignores only those errors specified. |
| verbose | boolean | If _true_ it turns verbose logging on for the task. |
| success | string | Task to run when the current task finishes without an error. |
| failure | string | Task to run when the current task finishes with an error. |
| complete | string | Task to run when the current task has finished without being cancelled.  |

## Error Handling

When a task has an error it will bubble up to all the tasks that ran before it unless the _ignoreError_ task argument is set to true. Tasks are also bubbled up from one workflow to another when called through the _workflowRun_ task.

### Task Errors

All tasks can return the following errors:

| Name | Description |
|------|-------------|
| Task_Error_MissingSubTask | Failed to find subtask. |
| Task_Error_MissingArg | Failed due to missing argument. |
| Task_Error_InvalidArg | Failed due to invalid argument. |
| Task_Error_Cancelled | Failed due to cancellation. |

### Platform Errors

The following error codes are used throughout the workflow engine.

| Name | Description |
|------|-------------|
| Platform_Error_None | No error. |
| Platform_Error_AccessInvalid | Invalid access to perform operation. |
| Platform_Error_AccessDenied | Denied access to perform operation. |
| Platform_Error_Locked | Cannot perform operation due to lock. |
| Platform_Error_Missing | Required resource was not found. |
| Platform_Error_NotEnoughSpace | Not enough space to perform operation. |
| Platform_Error_Unknown | Unknown error. |

# Task Types

Below is a list of all the supported task types.

  


## certStoreLoad

Load a certificate store valid for this workflow only

**************Version:************** 5.2

**Arguments:**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| **url** | string | URL/file of the thumbprint list/jwks file. (Should always be an https URL for a secure environment) |   
 |
| name | string | Name of the certificate store |   
 |

**Errors:**

| Name | Description |
|------|-------------|
| Json_Error_Authenticate | Failed to authenticate url content |
| Json_Error_Parse | Failed to parse url content |
| CertStore_Error_Load | Failed to load certificate store |

**JWKS Documentation**

Documentation of the file format can be found at [https://auth0.com/docs/jwks](https://auth0.com/docs/jwks)

**Thumbprint List Example:**

Key is the friendly name of the thumbprint, value is a base64 encoded thumbprint (sha1, sha224, sha256, sha384, sha512 supported)

```
{"qa.snxd.com": "teOGxFJgJJdpfxwD/soVGBQ6YX4=", "ssn": "teOGxFJgJJdpfxwD/soVGBQ6YX4=", "ssnqa": "iP8N+8Z4KJNZ8+5nm8J7efYruuU=", "ssntesting256mac": "+zHAcP1dSgIIn9Zdm3bPz2iIcyM="}
```

**Example:**

```
"trustJWKS":{"type": "certStoreLoad", "name": "hello", "url": "https://localhost/hello.jwks.json"}
```

  


## interopLoad

Loads an interop library.

**Version:** 5.1

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **name** | string | Friendly name for the interop library. |
| **path** | string | Path to the interop library to be loaded. |
| store | string/array | Certificate store used to authenticate (default: application's default interop store)Predefined certificate stores:

* app: Application certificate store
* platform: System certificate store
* null: Empty certificate store |
| * | key/value pairs | Options that get passed to interop as name.key=value |

**Changes in 5.2:**

* Added store argument

**Errors:**

| Name | Description |
|------|-------------|
| Interop_Error_Authenticate | Failed to authenticate the library. |
| Interop_Error_Load | Failed to load the library into memory. |

**Example:**

```
"loadPriority":{"type": "interopLoad", "name": "priority", "path": "{moduleDirectory}{libraryPrefix}priority.{libraryExtension}"}
```

## interopUnload

Unloads an interop library.

**Version:** 5.1

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **name**1 | string | Friendly name for the interop library. |
| **path**1 | string | Path to the interop library to be unloaded. |

**Additional Notes:**

1. Must be the same value that was used for interopLoad.**  
**

**Errors:**

| Name | Description |
|------|-------------|
| Interop_Error_Unload | Failed to unload the library from memory. |

**Example:**

```
"unloadPriority":{"type": "interopUnload", "name": "priority", "path": "{moduleDirectory}{libraryPrefix}priority.{libraryExtension}"}
```

## queue

List of workflow tasks to run. 

**Version:** 5.1

**Arguments:**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| **actions** | array of strings | List of task names to be executed. |   
 |
| concurrentActions | integer | Number of tasks to run in parallel. (-1 to run all tasks without queuing) | 1 |

**Status Variables:**

| Name | Type | Description |
|------|------|-------------|
| totalActions | integer | Total number of actions |
| runningActions | integer | Total number of actions running |
| completeActions | integer | Total number of actions complete |
| currentAction | integer | Index of action currently being processed. Only available if concurrentActions is 1. |

**Notes:**

1. When an action fails, no further actions are run.

**Changes in 5.2:**

* Added totalActions, runningActions, completeActions, currentAction status variables

**Example:**

```
"start":{"type": "queue", "concurrentActions": 1, "actions": [ "task1", "task2", "task3"]}
```

## aggregate

Queues a new task combined from the task in the workflow and a remote task or the args specified in content.

**Version:** 5.1

**Arguments:**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| **url**1 | string | URL to JSON object to aggregate. Should either contain a list of tasks and their arguments to merge, or be used in conjunction with the _target_ argument to specify the task to merge with. |   
 |
| **content**1 | object/string | Object or JSON string of object to aggregate. Maximum length as a string is 16384 characters. |   
 |
| source2 | string | Used to specify the path to merge from with-in the JSON object specified at the _url_. |   
 |
| target2 | string | Used to specify the task to merge with if the JSON object specified at the _url_ contains a dictionary of arguments. It is possible to also specify the path inside the task to merge at (e.g. mytask.config). |   
 |
| store | string/array | Certificate store used to authenticate (default: "app")Predefined certificate stores:

* app: Application certificate store
* platform: System certificate store
* null: Empty certificate storeIf this value is defined, it forces authenticate to true and requires content to be signed regardless of the protocol used to deliver it. |   
 |
| authenticate | boolean | If _true_ it will try to authenticate the signature in the JSON content, _false _otherwise. By default, it will authenticate the JSON on an HTTP connection and will not authenticate the JSON on a HTTPS connection because it is already secure. It will not try to authenticate a connection to the local{ContentUrl}webserver. | true |
| concurrentTasks | integer | Number of tasks to run in parallel. (-1 to run all tasks without queuing) | 1 |

**Additional Notes:**

1. _url_ or _content_ arguments are required (not both)
2. Only used in conjunction with _url_ argument

**Changes in 5.2:**

* Added store argument

**Errors:**

| Name | Description |
|------|-------------|
| Aggregate_Error_Parse | Failed to parse remote content. |
| Aggregate_Error_Authenticate | Failed to authenticate JSON. |
| Aggregate_Error_Merge | Failed to merge object. |
| WebGet_Error_* | WebGet errors. |
| Platform_Error_* | Platform errors. |

**Changes in 5.2:**

* Removed Aggregate_Error_Request error

**Example 1:**

workflow.json

```
"start":{"type": "aggregate", "url": "https://../example.json"},"logSomethingOne":{"type": "log"},"logSomethingTwo":{"type": "log"}
```

example.json:

```
{"logSomethingOne":{"message": "something One"}, "logSomethingTwo":{"message": "something Two"}}
```

**Example 2:**

workflow.json

```
"start":{"type": "aggregate", "content":{"logSomething": [{"message": "something One"},{"message": "something Two"},{"message": "something Three"},]}},"logSomething":{"type": "log"}
```

It is also possible to use a dictionary instead of a list the "logSomething" inside "content" if you are only aggregating a single task:

**Example 3:**

workflow.json

```
"start":{"type": "aggregate", "target": "logSomething", "url": "{contentUrl}aggregate.json"},"logSomething":{"type": "log"}
```

aggregate.json:

```
{"message": "something One"}
```

**Example 4:**

workflow.json

```
"start":{"type": "aggregate", "source": "path1.path2", "target": "logSomething", "url": "{contentUrl}aggregate.json"},"logSomething":{"type": "log"}
```

aggregate.json:

```
{"path1":{"path2":{"message": "something One"}}}
```

## error

Sets an error for the current task chain, or alternatively sets the exit code without shutting down.

**Version:** 5.1

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| exitCode | integer | Exit code to return from the program. |
| message | string | Error message to assign to task. |
| break | boolean | Break into system debugger. |

**Example:**

```
"caseOk":{"type": "error", "exitCode": 72},"caseNotOk":{"type": "error", "message": "Task_Error_Apocalypse", "exitCode": 666}
```

## shutdown

Stops further tasks from being run.

**Version:** 5.1

**Arguments:**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| exitCode | integer | Exit code to return from the program. |   
 |
| force | boolean | If _true_, it will not wait for task flow to finish before attempting to shutdown; when it does shutdown, any running tasks will be errored out with Task_Error_Cancelled. If _false_, it will attempt to wait for tasks to finish running before shutting down. Any tasks that are pending to be run will not be run except for the  unload task and its children. | false |
| removeLocalStorage | boolean | Removes the local storage directory when the application closes. | false |
| restartElevated | boolean | Restarts the application elevated. | false |
| restart | boolean | Restarts the application. | false |

**Example:**

```
"exit":{"type": "shutdown"}
```

## implode

Deletes the file on disk for the current process after exiting.

**Version:** 5.1.9

****Supported OS:**  
**

* Windows (not supported on UWP)
* Macintosh (does nothing)
* Linux (does nothing)

**Example:**

```
"implodeUponExit":{"type": "implode"}
```

## sleep

Waits for a specified time.

**Version:** 5.1

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **seconds** | string | Number of seconds to wait. |

**Example:**

```
"waitForTenSeconds":{"type": "sleep", "seconds": 10}
```

## log

Logs a specific message to the debug log.

**Version:** 5.1

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **message** | string | Text to log. |

**Example:**

```
"logToDebugLog":{"type": "log", "message": "Hello world!"}
```

## status

Updates the status for a specific object in the engine.

**Version:** 5.1

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **target** | string | Target object to update the status. This can be either a specific task or the workflow itself. |
| * | string | Status JSON to update. |

**Example:**

```
"updateParentTaskStatus":{"type": "status", "target": "{This.Parent}", "message": "Child task complete."}
```

## notification

Sends a NotificationCenter event. This task is useful for one-way communication between the workflow engine and the javascript or interop. For two-way communication consider a javascript or interop workflow task.

**Version:** 5.2

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **event** | string | Notification event following the format _Type.Notification_. |
| delay | number | Number of milliseconds to delay the event from being fired |
| content | object/string | Object or string containing information to send in event. |

**Example:**

workflow.json

```
"sendNotify":{"type": "notification", "event": "Yahoo.XYZ", "content":{"xyz": true, "filename": "{moduleFilename}"}},
```

main.js

```
notificationCenter.addObserver("Yahoo", "XYZ", function(sender, info){console.log("Triggered Yahoo.XYZ"); console.log(sender); console.log(info);});
```

## stringContains

See if one string contains another, either or botxh of which could be argument expansions.

**Version:** 5.1

**Arguments:**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| **stringOne** | string | String to search through. |   
 |
| **stringTwo** | string | String to find. |   
 |
| ignoreCase | boolean | _true_ to ignore case sensitivity when comparing strings, _false_ otherwise. | false |
| found | string | Task to run when stringOne contains stringTwo. |   
 |
| notFound | string | Task to run when stringOne does not contain stringTwo |   
 |

**Example:**

```
"isProcessorIntel":{"type": "stringContains", "stringOne": "{CPUVendor}", "stringTwo": "Intel", "found": "usingIntelProcessor", "notFound": "notUsingIntelProcessor"}
```

## stringCompare

Compare two strings, either or both of which could be argument expansions.

**Version:** 5.1

**Arguments:**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| **stringOne** | string | First string in comparison. |   
 |
| **stringTwo** | string | String to compare stringOne to. |   
 |
| ignoreCase | boolean | _true_ to ignore case sensitivity when comparing strings, _false_ otherwise. | false |
| equalTo | string | Task to run when values match. |   
 |
| notEqualTo | string | Task to run when values do not match, case regardless. |   
 |
| greaterThan | string | Task to run when stringOne > stringTwo. |   
 |
| lessThan | string | Task to run when stringOne < stringTwo. |   
 |

**Example:**

```
"isUserAdministrator":{"type": "stringCompare", "stringOne": "{userName}", "stringTwo": "Administrator", "equalTo": "installAsAdminUser", "notEqualTo": "installAsPlebian"}
```

## numberCompare

Compare two numbers, either or both of which could be argument expansions.

**Version:** 5.1

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **numberOne** | string | First number in comparison. |
| **numberTwo** | string | Number to compare numberOne to. |
| equalTo | string | Task to run when values match. |
| notEqualTo | string | Task to run when values do not match, case regardless. |
| greaterThan | string | Task to run when numberOne > numberTwo. |
| lessThan | string | Task to run when numberOne < numberTwo. |

**Example:**

```
"areOn64Bit":{"type": "numberCompare", "numberOne": "{SystemBitness}", "numberTwo": 64, "equalTo": "install64BitProduct" "notEqualTo": "areOn32Bit"}
```

## versionCompare

Compares two version numbers. A version number contains up to 4 numbers separated by periods or commas representing major, minor, release and build numbers.

Example of a switch key usage:

application.exe /action uninstall /key value

****Version:**** 5.1

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **versionOne** | string | First version in comparison. |
| **versionTwo** | string | Version to compare versionOne to. |
| equalTo | string | Task to run when values match. |
| notEqualTo | string | Task to run when key is missing, or value not equal. |
| greaterThan | string | Task to run when versionOne value > versionTwo value. |
| lessThan | string | Task to run when versionOne value < versionTwo value. |

**Example:**

```
"compareVersions":{"type":"versionCompare", "versionOne": "{CommandLine:installVersion}", "versionTwo": "2.3.0.1", "equalTo": "installed", "notEqualTo": "notInstalled"}
```

## processOpen

Opens an executable, a file, or a url using the default editor.

_This task automatically downgrades the elevation rights to "User"._

****Version: ****5.2 (previously known as "open" or "programOpen")

****Supported OS:**  
**

* Windows (not supported on UWP)
* Macintosh

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **path** | string | Path to the file/URL/executable to open. |

**Status Variables:**

| Name | Type | Description |
|------|------|-------------|
| path | string | Expanded path used in the arguments |

**Errors:**

| Name | Description |
|------|-------------|
| ProcessOpen_Error_Shell | Failed to open the specified file. |

**Changes in 5.2:**

* Added path status variable.

**Example:**

```
"browseToGoogle":{"type": "processOpen", "path": "http://www.google.com"}
```

## processIsOpen

Checks to see if a program is running, runs a task based on result.

********Version:******** 5.2 (previously known as "programIsOpen" in 5.1)

****Supported OS:**  
**

* Windows (not supported on UWP)
* Macintosh

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **path** | string | Path to the executable. |
| running | string | Task to run when program is running. |
| notRunning | string | Task to run when program is not running. |

**Status Variables:**

| Name | Type | Description |
|------|------|-------------|
| id | integer | Process id found |

**Example:**

```
"isProcessRunning":{"type": "processIsOpen", "path": "C:\\path\\to\\program.exe", "notRunning": "launchProcess", "running": "displayAlreadyRunning"}
```

## processClose

Closes a program based on its process id.

************Version:************ 5.2 (previously known as "programClose" in 5.1)

****Supported OS:**  
**

* Windows (not supported on UWP)
* Macintosh

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **id** | integer/string | ID of the process to close. |
| exitCode | integer | Exit code to terminate the process with. (Windows only) |
| closed | string | Task to run when program is closed. |
| notClosed | string | Task to run when program is not closed. |

**  
Example:**

```
"tryProcessClose":{"type": "processClose", "id": "{this.parent.status.id}"}
```

## processList

Enumerates processes. 

**************Version:************** 5.2

**Arguments:**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| parentId | integer | Only return children of a particular process ID, optional. |   
 |
| **forEach** | string | Task to run when a process is found |   
 |

**Status Variables:**

| Name | Type | Description |
|------|------|-------------|
| directory | string | Process directory |
| path | string | Full path to the process. |
| name | string | Process file name |
| id | integer | ID of process |
| parentId | integer | ID of parent process |

**Example:**

Enumerate all children:

```
"start":{"type": "processList", "next": "logProcessEntry"},"logProcessEntry":{"type": "log", "message": "Process -{this.parent.status.id}-{this.parent.status.path}"}
```

Enumerate all children of a certain process recursvely:

```
"start":{"type": "processList", "parentId": 56008, "forEach": "logProcessEntry"},"logProcessEntry":{"type": "log", "message": "{this.parent.status.id}-{this.parent.status.path}", "complete": "nextChildren"},"nextChildren":{"type": "processList", "parentId": "{this.parent.parent.status.id}", "forEach": "logProcessEntry"}
```

## launch

Launch an application.

************Version:************ 5.1

****Supported OS:**  
**

* Windows (not supported on UWP)
* Macintosh

**Arguments:**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| **path** | string | Path to application to run. |   
 |
| workingDirectory | string | Working directory for application. |   
 |
| arguments | string/array | Arguments for the application. If the value is an array of strings, they are encapsulated by double quotes and combined. |   
 |
| elevationRights | string | Required process elevation rights.

* "user": run as user
* "elevated": run as elevate user
* "asinvoker": run as the current process | user |
| waitForExit | boolean | Wait for the application to exit before completing. | false |
| verbose | boolean | Print out verbose debug information to log. | false |
| successCode | integer/array | Return code that indicates successful completion. | 0 |
| warningMap | object | Key/value pairs to match for an warning condition.  
The key is an exitCode and the value is the error string. |   
 |
| warningFlagsMap | object | Key/value pairs to match for an warning condition.  
The key is an exitCode flag and the value is the error string. |   
 |
| errorMap | object | Key/value pairs to match for an error condition.   
The key is an exitCode and the value is the error string. |   
 |
| errorFlagsMap | object | Key/value pairs to match for an error condition.   
The key is an exitCode flag and value is the error string. |   
 |
| successOutput | array | List of any strings to search for in stdout, for successful completion. (mac only) |   
 |
| errorOutputMap | object | Key/value pairs to match for an error condition. (mac only)  
The key is a string to search for in stdout, and the value is the error string. |   
 |
| showWindow | boolean | Show window for the target application. (windows only) | false |

**Status Variables:**

| Name | Type | Description |
|------|------|-------------|
| path | string | Path of the application that was launched. |
| arguments | string | Arguments used to launch the application. |

**Errors:**

| Name | Description |
|------|-------------|
| Launch_Error_Run | Error occurred while launching process. |
| Launch_Error_UnknownCode | Process returned unknown error code. |

**Example:**

```
"launchDontCareAboutReturn":{"type": "launch", "path": "{moduleDirectory}Downloads{pathSlash}popoff.exe", "waitForExit": false}"launchCheckForExitCode":{"type": "launch", "path": "{moduleDirectory}Downloads{pathSlash}application.exe", "waitForExit": true, "successCode": 102, "errorMap":{"101": "Application_Error_101", "102": "Application_Error_102"}}"launchCheckForStdout":{"type": "launch", "path": "/my/path/to/mymacbinary", "waitForExit": true, "successOutput": [ "COMPLETED SUCCESSFULLY", "NO ERRORS", "UPDATE SUCCESSFUL"], "errorOutputMap":{"INVALID ACCESS": "Application_Error_InvalidAccess", "BAD READ": "Application_Error_CannotRead"}}"launchWithAnalytics":{"type": "launch", "path": "{moduleDirectory}Downloads{pathSlash}popoff.exe", "waitForExit": false, "analytics":{"productName": "{productName:{this.status.path}}", "companyName": "{companyName:{this.status.path}}", "productVersion": "{productVersion:{this.status.path}}", "fileVersion": "{fileVersion:{this.status.path}}"}}
```

## macro

Load macros from a JSON URL or javascript object.

************Version:************ 5.1

**Arguments:**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| **url**1 | string | URL to JSON object to load |   
 |
| **key**1 | string | Macro name. |   
 |
| **value**1 | string/integer | Macro value. |   
 |
| **keyValuePairs**1 | string | Macro key/value pairs. |   
 |
| store | string/array | Certificate store used to authenticate (default: "app")Predefined certificate stores:

* app: Application certificate store
* platform: System certificate store
* null: Empty certificate storeIf this value is defined, it forces authenticate to true and requires content to be signed regardless of the protocol used to deliver it. |   
 |
| authenticate | boolean | If _true_ it will try to authenticate the signature in the JSON content, _false _otherwise. By default, it will authenticate the JSON on an HTTP connection and will not authenticate the JSON on a HTTPS connection because it is already secure. It will not try to authenticate a connection to the local{ContentUrl}webserver. |   
 |
| global | boolean | If _true_ the scope of the macro is app-wide, otherwise if _false_ the scope is__local to the current workflow. | false |

**Additional Notes:**

1. _url_ or _key/value _or_ keyValuePairs _arguments are required (not all)

**Changes in 5.2:**

* Added store, authenticate arguments

**Errors:**

| Name | Description |
|------|-------------|
| Macro_Error_Parse | Failed to parse remote content. |
| WebGet_Error_* | WebGet errors. |
| Platform_Error_* | Platform errors. |

**Changes in 5.2:**

* Removed Macro_Error_Request error

**Remote Example:**

```
"loadRemoteMacros":{"type": "macro", "url": "{ContentUrl}mymacros.json", "complete": "useMacro"},"useMacro":{"loadEnvironment": "{EnvironmentName}"}
```

mymacros.json

```
{"EnvironmentName": "live"}
```

**Local Example:**

```
"loadLocalMacros":{"type": "macro", "key": "environmentName", "value": "MacOSX"},"loadLocalMacros":{"type": "macro", "keyValuePairs":{"environmentName": "Windows NT", "environmentType": "VirtualMachine"}}
```

## analytics

Adds additional analytics properties to send for every event. 

************Version:************ 5.1.9

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **key**1 | string | Property name. |
| **value**1 | string/integer | Property value. |
| **keyValuePairs**1 | string | Property key/value pairs. |

**Additional Notes:**

1. _url_ or _key/value _or_ keyValuePairs _arguments are required (not all)

**Example:**

```
"extendAnalytics":{"type": "analytics", "keyValuePairs":{"os": "{SystemName}{SystemVersion}({SystemBitness}-bit)", "appVersion": "{AppVersion}"}}
```

Alternatively, each task supports an _analytics_ section which are additional properties to send for that task event. 

```
"myEvent":{"type": "myTask", "prop1": "strval1", "analytics":{"os": "{SystemName}{SystemVersion}({SystemBitness}-bit)", "appVersion": "{AppVersion}"}}
```

## urlRedirect

Redirect URL to another URL.

************Version:************ 5.1

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **beginsWith** | string/array of strings | Checks if the URL begins with this string before redirecting. |
| ** append**1 | string | Appends value to the existing URL . |
| ** replace**1 | string | Replaces the existing URL . |

**Additional Notes:**

1. _beginsWith_/_append_ or _beginsWith_/_replace_ arguments are required (not all).

**Example:**

```
"urlRedirectAppend":{"type": "urlRedirect", "beginsWith": "http://localhost/", "append": "?e={Add:{Time60},600}"},"urlRedirectReplace":{"type": "urlRedirect", "beginsWith": "http://localhost/index.html", "replace": "http://localhost/default.html"}
```

## urlRedirectMacro

Adds a custom macro to the URL redirection subsystem to be used by the urlRedirect task.

**************Version:************** 5.1.8

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **key**1 | string | Macro name. |
| **value**1 | string/integer | Macro value. (Supports task macros) |
| **keyValuePairs**1 | string | Macro key/value pairs. |

**Additional Notes:**

1. _key/value _or_ keyValuePairs _arguments are required (not all)

**Example:**

```
"urlRedirectMacro":{"type": "urlRedirectMacro", "key": "TokenAuthPrivateKey", "value": "MyPrivateKey", "complete": "urlRedirectAppend"},"urlRedirectAppend":{"type": "urlRedirect", "beginsWith": "http://localhost/", "append": "?e={Add:{Time60},600}{Copy:&t={MD5:{ThisUrlPath}&s={TokenAuthPrivateKey}}}"}
```

## registryKeyCreate

Create a registry key.

**************Version:************** 5.1

****Supported OS:**  
**

* Windows (not supported on UWP)
* Macintosh

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **hive** | string | Hive to read registry value from ("user", "machine", "root", "config", "desktopuser") |
| **location** | string | Location of the registry key. |
| view | string | Registry view ("default", "32", "64") |

**Errors:**

| Name | Description |
|------|-------------|
| RegistryKey_Error_Create | Failed to create the registry key. |

**Example:**

```
"addAppToRegistry":{"type":"registryKeyCreate", "hive": "machine", "location": "SOFTWARE\\Application1"}
```

## registryKeyDelete

Delete a registry key.

**************Version:************** 5.1

****Supported OS:**  
**

* Windows (not supported on UWP)
* Macintosh

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **hive** | string | Hive to read registry value from ("user", "machine", "root", "config", "desktopuser") |
| **location** | string | Location of the registry key. |
| view | string | Registry view ("default", "32", "64") |
| failIfMissing | boolean | If _true_ it reports an error when the key does not exist. |

**Errors:**

| Name | Description |
|------|-------------|
| RegistryKey_Error_Delete | Failed to delete the registry key. |

**Example:**

```
"removeAppFromRegistry":{"type":"registryKeyDelete", "hive": "machine", "location": "SOFTWARE\\Application1"}
```

## registryKeyExists

Check if a registry key exists.

**************Version:************** 5.1

****Supported OS:**  
**

* Windows (not supported on UWP)
* Macintosh

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **hive** | string | Hive to read registry value from ("user", "machine", "root", "config", "desktopuser") |
| **location** | string | Location of the registry key. |
| view | string | Registry view ("default", "32", "64") |
| exists | string | Task to run if the registry key exists. |
| missing | string | Task to run if the registry key is missing. |

**Example:**

```
"checkAppIsInstalled":{"type": "registryKeyExists", "hive": "machine", "location": "SOFTWARE\\Application1", "exists": "isInstalled", "missing": "isNotInstalled"}
```

## registryKeyRead

Reads registry keys.

**************Version:************** 5.1

****Supported OS:**  
**

* Windows (not supported on UWP)
* Macintosh

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **hive** | string | Hive to read registry value from ("user", "machine", "root", "config", "desktopuser") |
| **location** | string | Location of the registry key. |
| **key**1 | string | Registry key name. |
| **keys**1 | array of strings | Registry key names to read. |
| view | string | Registry view ("default", "32", "64") |
| security | string | Security group to add the key as ("default", "everybody") |
| read | string | Task to run when all keys were read successfully. |
| notRead | string | Task to run when one or more keys were not read. |

**Additional Notes:**

1. _key_/_value_ or _keys _arguments are required (not both)

**Status Variables:**

| Name | Type | Description |
|------|------|-------------|
| * | string | Values that were read. |

**Example:**

```
"readProductVersion":{"type":"registryKeyRead", "hive": "machine", "location": "SOFTWARE\\Application1", "key": "installedVersion", "success": "compareProductVersion"},"compareProductVersion":{"type":"stringCompare", "stringOne": "1.0", "stringTwo": "{this.parent.status.InstalledVersion}", "equalTo": "weHaveLatestVersion"}
```

## registryKeyWrite

Adds or edits registry keys.

**************Version:************** 5.1

****Supported OS:**  
**

* Windows (not supported on UWP)
* Macintosh

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **hive** | string | Hive to read registry value from ("user", "machine", "root", "config", "desktopuser") |
| **location** | string | Location of the registry key. |
| **key**1 | string | Registry key name. |
| **value**1 | string/integer | Registry key value. |
| **keyValuePairs**1 | key value pairs | Block of registry key value pairs. |
| view | string | Registry view ("default", "32", "64") |
| security | string | Security group to add the key as ("default", "everybody") |

**Additional Notes:**

1. _key_/_value_ or _keyValuePairs_ arguments are required (not both)

**Errors:**

| Name | Description |
|------|-------------|
| RegistryKey_Error_Write | Failed to write the registry key. |

**Example:**

```
"addProductVersion":{"type":"registryKeyWrite", "hive": "machine", "location": "SOFTWARE\\Application1", "key": "InstalledVersion", "value": "{AppVersion}"},"addProductInfo":{"type":"registryKeyWrite", "hive": "machine", "location": "SOFTWARE\\Application1", "keyValuePairs":{"Name": "Application1", "InstalledVersion": "{AppVersion}"}}
```

## iniRead

Reads a value from an .ini file.

**************Version:************** 5.1

**Arguments:**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| **path** | string | Path of the ini file to read. |   
 |
| section | string | Section of the ini file to retrieve setting from. | global |
| **key**1 | string | Name of the setting. |   
 |
| **keys**1 | string/array | Names of the settings to get. |   
 |
| read | string | Task to run if all of the requested keys were read. |   
 |
| notRead | string | Task to run if one or more of the requested keys were not read. |   
 |

**Additional Notes:**

1. _key_ or _keys_ arguments are required (not both)

**Status Variables:**

| Name | Type | Description |
|------|------|-------------|
| * | string | Values that were read. |

**Errors:**

| Name | Description |
|------|-------------|
| Ini_Error_Open | Failed to open the ini file for reading. |

**Example:**

```
"readValueFromIni":{"type": "iniRead", "path": "{userDesktop}test.ini", "section": "Settings", "key": "Option1", "complete": "displayValueFromIni"},"displayValueFromIni":{"type": "log", "message": "{this.parent.status.Option1}"},"readValuesFromIni":{"type": "iniRead", "path": "{userDesktop}test.ini", "section": "Settings", "keys": ["Option1", "Option2"], "complete": "displayValuesFromIni"},"displayValuesFromIni":{"type": "log", "message": "{this.parent.status.Option1}{this.parent.status.Option2}"},
```

## iniWrite

Writes a value to an .ini file.

**************Version:************** 5.1

**Arguments:**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| **path** | string | Path of the ini file to write to. |   
 |
| section | string | Section of the ini file to write setting to. | global |
| **key**1 | string | Name of the setting. |   
 |
| **value**1 | string | Value of the setting. |   
 |
| **keyValuePairs**1 | array | If setting multiple key value pairs this can be used. |   
 |

**Additional Notes:**

1. _key_/_value_ or _keyValuePairs_ arguments are required (not both)

**Errors:**

| Name | Description |
|------|-------------|
| Ini_Error_Save | Failed to write the ini file to disk. |

**Example:**

```
"writeIniFile":{"type": "iniWrite", "path": "{userDesktop}test.ini", "section": "Settings", "key": "Option1", "value": "Value1"}"writeMultipleToIniFile":{"type": "iniWrite", "path": "{userDesktop}test.ini", "section": "Settings", "keyValuePairs":{"test1": "test2", "test3": "test4", "test5": 10.4, "test6": "{moduleCurrentPath}testw.ini"}}
```

## plistRead

Reads values from a property list file.

**************Version:************** 5.1

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **path** | string | Path to the plist file. |
| **key**1 | string | Property key name. |
| **keys**1 | array of strings | Property key names to read. |
| read | string | Task to run when all keys were read successfully. |
| notRead | string | Task to run when one or more keys were not read. |

**Additional Notes:**

1. _key_/_value_ or _keys _arguments are required (not both)

**Status Variables:**

| Name | Type | Description |
|------|------|-------------|
| * | string | Values that were read. |

**Errors:**

| Name | Description |
|------|-------------|
| Plist_Error_Open | Failed to open plist file. |

**Example:**

```
"readProductInfo":{"type": "plistRead", "path": "{userDesktop}info.plist", "keys": ["CFBundleName","CFBundleVersion"], "complete": "logProductInfo"},"logProductInfo":{"type": "log", "message": "{this.parent.status.CFBundleName}{this.parent.status.CFBundleVersion}"},
```

## plistWrite

Adds or edits values in a property list file.

**************Version:************** 5.1

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **path** | string | Path to the plist file. |
| **key**1 | string | Property key name. |
| **value**1 | string/integer | Property key value. |
| **keyValuePairs**1 | key value pairs | Block of property key value pairs. |

**Additional Notes:**

1. _key_/_value_ or _keyValuePairs_ arguments are required (not both)

**Errors:**

| Name | Description |
|------|-------------|
| Plist_Error_Open | Failed to open plist file. |
| Plist_Error_Save | Failed to save plist to file. |

**Example:**

```
"writeProductInfo":{"type": "plistWrite", "path": "{userDesktop}info.plist", "key": "CFBundleName", "value": "1.0"},"writeProductInfos":{"type": "plistWrite", "path": "{userDesktop}info.plist", "keyValuePairs":{"CFBundleName": "host", "CFBundleVersion": "1.0"}}
```

## xmlRead

Reads values from an xml file.

**************Version:************** 5.1

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **path**1 | string | Path to the xml file. |
| **url**1 | string | URL to xml file |
| **key**2 | string | Xml key name. |
| **keys**2 | array of strings | Xml key names to read. |
| read | string | Task to run when all keys were read successfully. |
| notRead | string | Task to run when one or more keys were not read. |

**Additional Notes:**

1. _path_ or _url_ arguments are required (not both)
2. _key_/_value_ or _keys _arguments are required (not both)

**Status Variables:**

| Name | Type | Description |
|------|------|-------------|
| * | string | Values that were read. |

**Errors:**

| Name | Description |
|------|-------------|
| Xml_Error_Open | Failed to open xml file. |
| Xml_Error_Parse | Failed to parse xml content. |
| WebGet_Error_* | WebGet errors. |
| Platform_Error_* | Platform errors. |

**Changes in 5.2:**

* Added url argument
* Added Xml_Error_Parse error

**Example:**

Xml:

```
<?xml version="1.0" ?><catalog> <book id="bk101"> <author>Gambardella, Matthew</author> <title>XML Developer's Guide</title> <genre>Computer</genre> <price>44.95</price> <publish_date>2000-10-01</publish_date> <description>An in-depth look at creating applications with XML.</description> </book></catalog>
```

Workflow:

```
"readAttribute":{"type": "xmlRead", "path": "{userDesktop}test.xml", "key": "catalog.book.-id", "complete": "logAttribute"},"logAttribute":{"type": "log", "message": "{this.parent.status.-id}"},"readElement":{"type": "xmlRead", "path": "{userDesktop}test.xml", "key": "catalog.book.author", "complete": "logElement"},"logElement":{"type": "log", "message": "{this.parent.status.author}"},
```

## xmlWrite

Adds or edits values in a xml file.

**************Version:************** 5.1

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **path** | string | Path to the xml file. |
| **key**1 | string | Xml key name |
| **value**1 | string/integer | Xml key value. |
| **keyValuePairs**1 | key value pairs | Block of xml key value pairs. |

**Additional Notes:**

1. _key_/_value_ or _keyValuePairs_ arguments are required (not both)

**Errors:**

| Name | Description |
|------|-------------|
| Xml_Error_Open | Failed to open xml file. |
| Xml_Error_Save | Failed to save xml to file. |

**Example:**

Xml:

```
<?xml version="1.0" ?><catalog> <book id="bk101"> <author>Gambardella, Matthew</author> <title>XML Developer's Guide</title> <genre>Computer</genre> <price>44.95</price> <publish_date>2000-10-01</publish_date> <description>An in-depth look at creating applications with XML.</description> </book></catalog>
```

Workflow:

```
"writeXmlAttribute":{"type": "xmlWrite", "path": "{userDesktop}test.xml", "key": "catalog.book.-id", "value": "bk100"},"writeXmlElement":{"type": "xmlWrite", "path": "{userDesktop}test.xml", "keyValuePairs":{"catalog.book.modifiedDate": "10/12/17", "catalog.book~.-id": "bk103", "catalog.book[-id=bk103].author": "Nate The Great", "catalog.book[-id=bk103].title": "Superman"}}
```

## jsonRead

Reads values from an json file.

**************Version:************** 5.1.8

**Arguments:**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| **path**1 | string | Path to the json file. |   
 |
| **url**1 | string | URL to the json file. |   
 |
| **content1** | object/string | Object or JSON string. |   
 |
| **key**2 | string | Json key name. |   
 |
| **keys**2 | array of strings | Json key names to read. |   
 |
| store | string/array | Certificate store used to authenticate (default: "app")Predefined certificate stores:

* app: Application certificate store
* platform: System certificate store
* null: Empty certificate storeIf this value is defined, it forces authenticate to true and requires content to be signed regardless of the protocol used to deliver it. |   
 |
| authenticate | boolean | If _true_ it will try to authenticate the signature in the JSON content, _false _otherwise. By default, it will authenticate the JSON on an HTTP connection and will not authenticate the JSON on a HTTPS connection because it is already secure. It will not try to authenticate a connection to the local{ContentUrl}webserver.  | true |
| read | string | Task to run when all keys were read successfully. |   
 |
| notRead | string | Task to run when one or more keys were not read. |   
 |

**Additional Notes:**

1. _path_ or _url_ or _content_ arguments are required (not both)
2. _key_/_value_ or _keys _arguments are required (not both)

**Changes in 5.2:**

* Added store argument

**Status Variables:**

| Name | Type | Description |
|------|------|-------------|
| * | string | Values that were read. |

**Errors:**

| Name | Description |
|------|-------------|
| Json_Error_Open | Failed to open json file |
| Json_Error_Parse | Failed to parse json content |
| WebGet_Error_* | WebGet errors. |
| Platform_Error_* | Platform errors. |

**Changes in 5.2:  
**

* Added content argument
* 

Added url argument
* 

Added JSON_Error_Parse error

**Example:**

JSON:

```
{"catalog":{"bk101":{"author": "Gambardella, Matthew", "title": "XML Developer's Guide", "genre": "Computer", "price": 44.95, "publishDate": "2000-10-01", "description": "An in-depth look at creating applications with XML."}}}
```

Workflow:

```
"readValue":{"type": "jsonRead", "path": "{userDesktop}test.json", "key": "catalog.bk101.author", "complete": "logValue"},"logValue":{"type": "log", "message": "{this.parent.status.author}"},
```

## jsonWrite

Adds or edits values in a json file.

**************Version:************** 5.1.8

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **path** | string | Path to the json file. |
| **key**1 | string | Json key name |
| **value**1 | string/integer | Json key value. |
| **keyValuePairs**1 | key value pairs | Block of json key value pairs. |

**Additional Notes:**

1. _key_/_value_ or _keyValuePairs_ arguments are required (not both)

**Errors:**

| Name | Description |
|------|-------------|
| Json_Error_Open | Failed to open json file |
| Json_Error_Save | Failed to save json to file |

**Example:**

JSON:

```
{"catalog":{"bk101":{"author": "Gambardella, Matthew", "title": "XML Developer's Guide", "genre": "Computer", "price": 44.95, "publishDate": "2000-10-01", "description": "An in-depth look at creating applications with XML."}}}
```

Workflow:

```
"writeJsonValue":{"type": "jsonWrite", "path": "{userDesktop}test.json", "key": "catalog.bk101.modifiedDate", "value": "2001-10-10"}
```

## fileCopy

Copies files from one location to another on disk.

**************Version:************** 5.1

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| sourcePath | string | Source file to copy. |
| targetPath | string | Target file to copy to. |
| _move_ | _boolean_ | _DEPRECATED. Delete source file when copying complete._ |

**Example:**

```
"copyFilesToDesktop":{"type": "fileCopy", "sourcePath": "{moduleDirectory}source.exe", "targetPath": "{userDesktop}target.exe"}
```

## fileMove

Moves files from one location to another on disk.

**************Version:************** 5.1

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| sourcePath | string | Source file to move. |
| targetPath | string | Target file to move to. |
| failIfNotDeleted | boolean | Causes task to fail if the source is not deleted. |

**Example:**

```
"moveFilesToDesktop":{"type": "fileMove", "sourcePath": "{moduleDirectory}source.exe", "targetPath": "{userDesktop}target.exe"}
```

## fileDelete

Deletes a file from the file system. If the specified file does not exists, the task will succeed.

**************Version:************** 5.1

**Arguments:**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| **path** | string | Path of file to be erased. |   
 |
| waitForReboot | boolean | Wait for reboot to erase. Requires elevation. | false |
| failIfMissing | boolean | If _true_ it reports an error when the file does not exist. |   
 |

**Example:**

```
"deleteExample":{"type": "fileDelete", "path": "{moduleDirectory}example{pathSlash}example.file"}
```

## fileExists

Check if a file exists on the file system. 

**************Version:************** 5.1

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **path** | string | Path of file to check existance. |
| exists | string | Task to run if the file exists. |
| missing | string | Task to run if the file is missing. |

**Example:**

```
"checkExample":{"type": "fileExists", "path": "{moduleDirectory}example{pathSlash}test.txt", "missing": "downloadExample"}
```

## fileHash

Gets or compares the hash of a file on disk. 

**************Version:************** 5.1.3

**Arguments:**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| **path** | string | Path of file to hash. |   
 |
| algorithm | string | Name of the hash interface:

* crc
* md2, md4, md5
* sha1, sha224, sha256, sha384, sha512 | sha1 |
| expectedDigest | string | Expected hash digest. |   
 |
| equalTo | string | Task to run if the actual hash equals the expected hash. |   
 |
| notEqualTo | string | Task to run if the actual has does not equal the expected hash. |   
 |

**Additional Notes:**

* If expectedDigest is an empty string, the task will complete successfully without equalTo or notEqual subactions being called**.**

**Status Variables:**

| Name | Type | Description |
|------|------|-------------|
| actualDigest | string | Actual digest of the file on disk. |
| expectedDigest | string | Digest that was expected. |

**Example:**

```
"checkFileHash":{"type": "fileHash", "path": "{moduleDirectory}app.exe", "algorithm": "md5", "expectedDigest": "9569052415bfa09d411a0aaedf5acbd6", "equalTo": "fileIsCorrect", "notEqualTo": "fileIsCorrupt"}"getFileHash":{"type": "fileHash", "path": "{moduleDirectory}app.exe", "algorithm": "md5", "complete": "logFileHash"},"logFileHash":{"type": "log", "message": "{this.parent.status.ExpectedDigest}vs{this.parent.status.ActualDigest}"}
```

## fileAuthenticate

Authenticates the signature of a file on disk. 

**************Version:************** 5.1.3

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **path** | string | Path of file to authenticate.Windows

* To pass authentication, must be a valid code-signed PE formatted binary.Macintosh

* To pass authentication, must be a valid code-signed MachO binary. |
| store | string/array | Certificate store used to authenticate (default: "app")Predefined certificate stores:

* app: Application certificate store
* platform: System certificate store
* null: Empty certificate store |
| valid | string | Task to run when file passes authentication. |
| notValid | string | Task to run when file does not pass authentication. |

**Changes in 5.2:**

* Added store argument

**Example:**

```
"checkSignature":{"type": "fileAuthenticate", "path": "{moduleDirectory}app.exe", "valid": "fileIsOkToRun", "notValid": "fileIsNotOkToRun"}
```

## directoryCreate

Creates a directory on the file system.

**************Version:************** 5.1

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **path** | string | Path of directory to create. |

**Example:**

```
"createExample":{"type": "directoryCreate", "path": "{moduleDirectory}example"}
```

## directoryCopy

Copies the contents of a directory from one location to another. 

**************Version:************** 5.1.8

**Arguments:**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| **sourcePath** | string | Path of directory whose contents to copy. |   
 |
| **targetPath** | string | Path to copy contents of source directory to. |   
 |
| overwrite | boolean | If _true_ it will overwrite existing files. | true |
| recurse | boolean | If _true_ it will copy the directory recursively. | true |

**Changes in 5.2:**

* Added overwrite argument

**Example:**

```
"copyFolder":{"type": "directoryCopy", "sourcePath": "{moduleDirectory}example", "targetPath": "{moduleDirectory}example2", "recurse": true}
```

## directoryMove

Moves the contents of a directory from one location to another. 

**************Version:************** 5.1.8

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **sourcePath** | string | Path of directory whose contents to move. |
| **targetPath** | string | Path to move contents of source directory to. |

**Example:**

```
"moveFolder":{"type": "directoryMove", "sourcePath": "{moduleDirectory}example", "targetPath": "{moduleDirectory}example2"}
```

## directoryDelete

Delete a directory from the file system. If the specified directory does not exist, the task will succeed.

**************Version:************** 5.1

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **path** | string | Path of directory to erase. |
| failIfMissing | boolean | If _true_ it reports an error when the directory does not exist. |
| onlyIfEmpty | boolean | If _true_ it will only delete the directory if it is empty. |

**Example:**

```
"deleteExample":{"type": "directoryDelete", "path": "{moduleDirectory}example"}
```

## directoryList

Gets a directory listing. 

**************Version:************** 5.2

**Arguments:**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| **path** | string | Search path which can contain wildcards. |   
 |
| skipHidden | boolean | Skip hidden files and directories | true |
| skipReadOnly | boolean | Skip read only files and directories | false |
| forEachFile | string | Task to run when a file is found |   
 |
| forEachDirectory | string | Task to run when a directory is found |   
 |

**Status Variables:**

| Name | Type | Description |
|------|------|-------------|
| directory | string | Search directory |
| path | string | Full path to the file or directory found. |
| name | string | Name of the entry |
| modifiedTime | integer | Modified time of entry |
| creationTime | integer | Creation time of entry |
| size | integer | Size of entry |
| hidden | integer | 1 if hidden, 0 otherwise |
| readonly | integer | 1 if read only, 0 otherwise. |

**Example:**

```
"logFile":{"type": "log", "message": "file{this.parent.status.path}- mtime{this.parent.status.modifiedTime}- ctime{this.parent.status.creationTime}- size{this.parent.status.size}"},"logDirectory":{"type": "log", "message": "directory -{this.parent.status.path}- mtime{this.parent.status.modifiedTime}- ctime{this.parent.status.creationTime}- size{this.parent.status.size}"},"start":{"type": "directoryList", "path": "{systemDrive}", "forEachFile": "logFile", "forEachDirectory": "logDirectory"}
```

**Recursive Example:**

```
"printFiles":{"type": "log", "message": "file -{this.parent.status.path}- mtime{this.parent.status.modifiedTime}ctime -{this.parent.status.creationTime}size -{this.parent.status.size}"},"printDirectories":{"type": "log", "message": "directory -{this.parent.status.path}- mtime{this.parent.status.modifiedTime}ctime -{this.parent.status.creationTime}size -{this.parent.status.size}", "path": "{this.parent.status.path}", "success": "listNextDirectory"},"listNextDirectory":{"type": "directoryList", "path": "{this.parent.parent.status.path}", "forEachFile": "printFiles", "forEachDirectory": "printDirectories"},"listSystemDrive":{"type": "directoryList", "path": "{systemDrive}", "forEachFile": "printFiles", "forEachDirectory": "printDirectories"},"start":{"type": "queue", "concurrentActions": 1, "actions": [ "listSystemDrive"]}
```

## directoryExists

Check if a directory exists on the file system.

**************Version:************** 5.1

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **path** | string | Path of directory to check existance. |
| exists | string | Task to run if the directory exists. |
| missing | string | Task to run if the directory is missing. |

**Example:**

```
"checkDir":{"type": "directoryExists", "path": "{moduleDirectory}example", "exists": "updateExample"}
```

## directoryIsEmpty

Check if a directory is empty.

**************Version:************** 5.1.3

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **path** | string | Path of directory to check. |
| failIfMissing | boolean | If _true_ it reports an error when the directory does not exist. |
| empty | string | Task to run if the directory is empty. |
| notEmpty | string | Task to run if the directory is not empty. |

**Example:**

```
"checkDirIsEmpty":{"type": "directoryIsEmpty", "path": "{moduleDirectory}example", "empty": "deleteDir"}
```

## directoryIsWritable

Check if a directory is writable by the current process.

**************Version:************** 5.1.8

**Supported OS:**

* Windows (not supported on UWP)
* Macintosh
* Linux

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **path** | string | Path of directory to check for write permissions. |
| recurse | boolean | If directory does not exist and _true,_ it finds the nearest parent directory that exists and verifies it has write permissions on it. |
| writable | string | Task to run if the directory is writable. |
| notWritable | string | Task to run if the directory is not writable. |

**Example:**

```
"checkDirIsWritable":{"type": "directoryIsWritable", "path": "{moduleDirectory}example", "writable": "installFiles", "notWritable": "installFilesElevated"}
```

## diskSpaceCheck

Checks the disk space on a certain path.

**************Version:************** 5.1

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **requiredBytes** | int | Number of bytes required to successfully complete the task. |
| path | string | Path of the file system to check for free space. |
| enough | string | Task to run when there is enough space on the disk. |
| notEnough | string | Task to run when there is not enough space on the disk. |

**Example:**

```
"checkDiskSpaceOnCDrive":{"type": "diskSpaceCheck", "path": "c:\", "requiredBytes": 129199967040, "enough": "installApp", "notEnough": "notifyUser"}
```

## msi

Runs an MSI installer.

**************Version:************** 5.1

****Supported OS:**  
**

* Windows (not supported on UWP)

**Arguments:**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| **path** | string | Path to the .msi installer file. |   
 |
| silent | boolean | If the install should be silent. | true |
| properties | object | Custom key/value pair properties for the installer. Your specific MSI installer must support these. Values cannot contain spaces. |   
 |
| reportStatus | boolean | Shows MSI status for the task if _true_, _false_ otherwise. | true |
| reportProgress | boolean | Shows MSI progress for the task if _true_, _false_ otherwise. | true |
| logFilename | string | Filename to where the .msi should save a log to. |   
 |

**Errors:**

| Name | Description |
|------|-------------|
| Msi_Error_Install | An installer error has occurred. |

**Example:**

```
"installDownload":{"type": "msi", "silent": true, "path": "{this.parent.status.outputPath}", "arguments": ""}
```

## wmi

Queries the Windows Management Instrumentation service.

**************Version:************** 5.1.3

****Supported OS:**  
**

* Windows (not supported on UWP)

**Arguments:**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| **query** | string | WQL query. |   
 |
| **key1** | string | Name of the property to retrieve. |   
 |
| **keys**1 | string/array | Names of the properties to retrieve. |   
 |
| server | string | Name of the server. | root\cimv2 |
| matched | string | Task to run if matches were found for the requested query. |   
 |
| notMatched | string | Task to run if no matches were found for the requested query. |   
 |

**Additional Notes:**

1. _key_ or _keys_ arguments are required (not both)

**Errors:**

| Name | Description |
|------|-------------|
| Wmi_Error_Create | Failed to create wmi object. |

**Example:**

```
"getMemoryInfo":{"type": "wmi", "query": "SELECT * FROM Win32_PhysicalMemory", "key": "DeviceLocator", "complete": "logMemoryInfo"},"logMemoryInfo":{"type": "log", "message": "{this.parent.status.Items[0].DeviceLocator}"},"getProcessorInfo":{"type": "wmi", "query": "SELECT * FROM Win32_Processor", "keys": ["Family", "Architecture"], "complete": "logProcessorInfo"},"logProcessorInfo":{"type": "log", "message": "Arch:{this.parent.status.Items[0].Architecture}Fam:{this.parent.status.Items[0].Family}"}
```

## restorePoint

Sets a restore point.

**************Version:************** 5.1.8 (previously known as "restorePointBegin")

****Supported OS:**  
**

* Windows (elevation required, not supported on UWP)

**Arguments:**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| **name** | string | Name of the restore point, usually the name of the app being installed. |   
 |
| **actions**1 | array of strings | List of task names to be executed. |   
 |
| operation | string | The operation occurring that requires a restore point.

* install
* uninstall | install |
| nested | boolean | _True_ if it is a nested restore point, _false_ otherwise. | false |

**Notes:**

1. Starts the restore point before the actions are executed. If any of the actions fails, the restore point is cancelled. If all the actions succeed, then the restore point ends.

**Errors:**

| Name | Description |
|------|-------------|
| RestorePoint_Error_Set | Failed to set system restore point. |

**Example:**

```
"setRestorePoint-win":{"type": "restorePoint", "status": "UI_CreatingRestorePoint", "operation": "install", "name": "{productName}", "concurrentTasks": 1, "actions": [ "task1", "task2"]}
```

## shortcutCreate

Creates a shortcut. 

**************Version:************** 5.1

**Supported OS:**

* Windows (not supported on UWP)
* Linux

**Arguments:**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| **name** | string | Display name of the shortcut. (ie. "Game Map Editor") |   
 |
| **path** | string | Path to the application that the shortcut will run. |   
 |
| arguments | string/array | Arguments for the application. If the value is an array of strings, they are encapsulated by double quotes and combined. (Windows only) |   
 |
| location | string | Target directory to create the shortcut in. | {userDesktop} |
| iconLocation | string | Path to the application/library that contains the icon. (Windows only)  
If no icon location is specified, the path to the application will be used. |   
 |
| iconIndex | number | Index of the icon. (Windows only) |   
 |
| runAsAdmin | boolean | Set to true, to create a link that runs the application as an administrator. (Windows only) |   
 |

**Errors:**

| Name | Description |
|------|-------------|
| Shortcut_Error_Create | Failed to create shortcut. |

**Example:**

```
"createDesktopShortcut":{"type": "shortcutCreate", "name": "MyApp", "path": "{ProgramFiles}MyApp2\\myapp2.exe"}
```

## shortcutDelete

Deletes a shortcut.

**************Version:************** 5.1

****Supported OS:**  
**

* Windows (not supported on UWP)
* Linux

**Arguments:**

| Name | Type | Description |   
 |
|------|------|-------------|-----|
| **name** | string | Display name of the shortcut. (ie. "Game Map Editor") |   
 |
| location | string | Directory the shortcut is located in. | {userDesktop} |

**Errors:**

| Name | Description |
|------|-------------|
| Shortcut_Error_Delete | Failed to delete shortcut. |

**Example:**

```
"deleteDesktopShortcut":{"type": "shortcutDelete", "name": "MyApp"}
```

## pkg

Runs a PKG installer. This task inherits the properties of the _launch_ task.

**************Version:************** 5.1

****Supported OS:**  
**

* Macintosh

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **path** | string | Path to the .pkg installer file. |
| arguments | string/array | Arguments for the installer. If the value is an array of strings, they are encapsulated by double quotes and combined. |
| logFilename | string | Filename to where the .pkg should save a log to. |
| logOnlyErrors | boolean | Set to true if you only want to log the errors to the log file. |

**Example:**

```
"installDownload":{"type": "pkg", "path": "{this.parent.status.OutputDirectory}Application1.pkg", "elevationRights": "elevated"}
```

## dmgMount

Mounts an apple disk image.

**************Version:************** 5.1

****Supported OS:**  
**

* Macintosh

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **path** | string | Path to the .dmg file to mount |
| target | string | Target name to mount to. For example, specifying "MyProduct" would mount to "/Volumes/MyProduct". When no target is specified, the dmg is mounted to /Volumes/{SHA1:path}/. |

**Errors:**

| Name | Description |
|------|-------------|
| DiskImage_Error_Launch | Failed to launch disk image utility. |
| DiskImage_Error_Mount | Failed to mount disk image. |

**Example:**

```
"mountMyProductDmg":{"type": "dmgMount", "path": "{this.parent.status.OutputDirectory}product.dmg"}
```

## dmgUnmount

Unmounts an apple disk image.

**************Version:************** 5.1

****Supported OS:**  
**

* Macintosh

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| **path** | string | Path to the .dmg file to unmount |
| target | string | Target name to unmount. For example, specifying "MyProduct" would unmount "/Volumes/MyProduct". When no target is specified, the dmg unmounted is /Volumes/{SHA1:path}/. |

**Errors:**

| Name | Description |
|------|-------------|
| DiskImage_Error_Launch | Failed to launch disk image utility. |
| DiskImage_Error_Mount | Failed to mount disk image. |

**Example:**

```
"unmountMyProductDmg":{"type": "dmgUnmount", "path": "{this.parent.status.OutputDirectory}product.dmg"}
```

## unzip

Unzips a file on disk

**************Version:************** 5.1

**Arguments:**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| **path** | string | Filename of the zip file to operate on. |   
 |
| **pathInZip** | string | Name of the file in the zip to extract. (wildcards are supported) | * |
| **outputDirectory** | string | Directory where the file(s) will be extracted. |   
 |
| password | string | Password for archive |   
 |

**Status Variables:**

| Name | Type | Description |
|------|------|-------------|
| pathInZip | string | Path of the file being extracted in the zip. |
| outputPath | string | Path of the file being extracted on disk. |

**Changes in 5.2:  
**

* Added password argument for encrypted archives
* Added support for AES encrypted archives

**Example:**

```
"unzipDownload":{"type": "unzip", "path": "{this.parent.status.OutputPath}", "pathInZip": "*", "outputDirectory": "{userDesktop}"}
```

## download

Downloads a file to disk or loads a JSON object into the current task's status dictionary.

**************Version:************** 5.1.2

**Arguments:**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| **url** | string | URL to download. |   
 |
| outputPath | string | Name of the file on disk to save to. |   
 |
| headers | key/value pairs | Additional request headers to send. |   
 |
| timeout | number | Number of seconds to wait for a socket _read _before timing out. This is not a socket _connect_ timeout. | 15 |
| maxRetries | number | Number of times to retry after the first error. | 0 |
| allowProxy | boolean | If _true_ it will allow connections through a proxy, _false_ otherwise. | true |
| allowResume | boolean | If _true_ it will allow the output file to resume downloading, _false_ will always overwrite the output file. | false |
| skipTimestamp | boolean | Whether or not to skip syncing the timestamp from the server to the files downloaded on disk. If _true_, the file on disk will have the modified date of the time they were created, otherwise it will have the modified date as specified by the remote server. | false |
| overwriteIfNewer | boolean | If _true_ it will overwrite the local file with the remote file if the remote file is newer than the local file.   
Requires allowResume to be _true _and _skipTimestamp_ to be _false_. | false |
| overwriteIfOlder | boolean | If _true_ it will overwrite the local file with the remote file if the remote file is older than the local file.   
Requires allowResume to be _true_ and_ skipTimestamp_ to be _false_. | false |
| limitBodySize | number | If greater than zero, it specifies the maximum number of bytes that can be downloaded in the response body. |   
 |

**Status Variables:**

| Name | Type | Description |
|------|------|-------------|
| name | string | Filename of URL |
| paused | boolean | Whether or not the download is paused. |
| active | boolean | Whether or not the download is downloading. |
| completeBytes | number | Number of bytes completed. |
| totalBytes | number | Number of bytes total in download. |
| existingBytes | number | Number of bytes already downloaded. |
| remainingTime | number | Number of seconds remaining for download. |
| remainingBytes | number | Number of bytes remaining to download. |
| remoteReadBytes | number | Number of bytes downloaded. |
| remoteWriteBytes | number | Number of bytes uploaded. |
| remoteReadSpeed | number | Number of bytes downloaded per second. |
| remoteWriteSpeed | number | Number of bytes uploaded per second. |
| remoteAvgReadSpeed | number | Average number of bytes downloaded per second. |
| remoteAvgWriteSpeed | number | Average number of bytes uploaded per second. |
| remoteMaxReadSpeed | number | Maximum number of bytes downloaded per second. |
| remoteMaxWriteSpeed | number | Maximum number of bytes uploaded per second. |
| activeTime | number | Seconds download was active. |
| pauseTime | number | Seconds download was paused. |
| outputPath | string | Output file's full path. |
| outputFilename | string | Output file's name. |
| outputDirectory | string | Output file's directory. |
| responseCode | number | HTTP response status code |
| responseVersion | string | HTTP response status version |
| responseMessage | string | HTTP response status message |
| responseHeaders | object | HTTP response headers |

**Errors:**

| Name | Description |
|------|-------------|
| Download_Error_Parse | Failed to parse JSON. |
| Download_Error_Authenticate | Failed to authenticate JSON. |
| WebGet_Error_* | WebGet errors. |
| Platform_Error_* | Platform errors. |

**Changes in 5.2:**

* Added status variables
  * active, activeTime, pauseTime, totalBytes, completeBytes, existingBytes
  * responseCode, responseVersion, responseMessage, responseHeaders
* Added skipTimestamp, overwriteIfNewer, overwriteIfOlder, and maxRetries arguments
* Removed json and authenticateJson argument (use JSONRead task instead)

**Example:**

```
"downloadUbuntu":{"type": "download", "url": "http://releases.ubuntu.com/16.04.1/ubuntu-16.04.1-desktop-amd64.iso", "outputPath": "{userDesktop}ubuntu-16.04.1-desktop-amd64.iso" "headers":{"test11": "value2", "test22": "{moduleDirectory}"}}
```

## repositorySync

Updates an existing repository

**************Version:************** 5.1

**Arguments:**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| allowPartial | bool | Allows cancelling before sync is complete. | true |
| repair | bool | Repair the repository1 |   
 |
| store | string/array | Certificate store used to authenticate (default: "app")Predefined certificate stores:

* app: Application certificate store
* platform: System certificate store
* null: Empty certificate store |   
 |
| * |   
 | Additional repository arguments |   
 |

**Additional Notes: **

1. Tasks with _repair_ enabled will ignore the source and mask fields if returned by the catalog file, so that whole pieces are used to repair the filesystem and no pieces are skipped. 

See [](5.1 Repository.md) documentation for additional arguments. 

**Changes in 5.2:**

* Added store argument

**Example:**

```
"sync":{"type": "repositorySync", "repository": "gameclient", "metafile": "{moduleDirectory}Download{pathSlash}gameclient-meta.json", "local":{"type": "file", "path": "{moduleDirectory}Download"}, "backup":{"type": "filePiece", "path": "{moduleDirectory}Download{pathSlash}Backup"}"status": "UI_Updating", "success": "syncComplete"},"repair":{"type": "repositorySync", "repository": "gameclient", "metafile": "{moduleDirectory}Download{pathSlash}gameclient-meta.json", "local":{"type": "file", "path": "{moduleDirectory}Download"}, "backup":{"type": "filePiece", "path": "{moduleDirectory}Download{pathSlash}Backup"}"repair": true, "status": "UI_Repairing", "success": "syncComplete"}
```

## repositoryCheck

Checks to see if an existing repository needs to be updated.

**************Version:************** 5.1

**Arguments:**

| Name | Type | Description |
|------|------|-------------|
| check | bool | Dry run - only check if update needs to occur. |
| install | string | Task to run if install required. |
| update | string | Task to run if update required. |
| upToDate | string | Task to run if and install or update is not required. |
| store | string/array | Certificate store used to authenticate (default: "app")Predefined certificate stores:

* app: Application certificate store
* platform: System certificate store
* null: Empty certificate storeIf this value is defined, it forces authenticate to true and requires content to be signed regardless of the protocol used to deliver it. |

  
See [](5.1 Repository.md) documentation for additional arguments. 

**Changes in 5.2:**

* Added store argument

**Example: **

```
"syncIfNeeded":{"type": "repositoryCheck", "repository": "gameClient", "metafile": "{moduleDirectory}Download{pathSlash}gameclient-meta.json", "update": "updateGame", "install": "installGame", "upToDate": "syncComplete"}
```

## repositoryFileCheck

Checks to see if an existing repository needs to be repaired by examining the existance, size, and modified timestamp of the files on disk.

**************Version:************** 5.1.9

**Arguments:**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| **metafile** | string | Path to the repository metafile. |   
 |
| **path** | string | Path to the local files on disk. |   
 |
| timestamp | bool | Compare modified time stamps. | true |
| valid | string | Task to run if all files on disk match. |   
 |
| notValid | string | Task to run if files on disk do not match. |   
 |

**Errors:**

| Name | Description |
|------|-------------|
| RepositoryFileCheck_Error_MetaFile | Failed to open or read metafile. |

**Example: **

```
"repairIfNeeded":{"type": "repositoryFileCheck", "metafile": "{moduleDirectory}Download{pathSlash}gameclient-meta.json", "path": "{repositoryDirectory}", "valid": "syncComplete" "notValid": "repairGame"}
```

## repositoryErase

Erase an existing repository.

**************Version:************** 5.1

**Example: **

See [](5.1 Repository.md) documentation for additional arguments. 

```
"erase":{"type": "repositoryErase", "repository": "gameclient", "metafile": "{moduleDirectory}Download{pathSlash}gameclient-meta.json", "local":{"type": "file", "path": "{moduleDirectory}Download"}, "backup":{"type": "filePiece", "path": "{moduleDirectory}Download{pathSlash}Backup"}}
```

## progress

Unified progress for multiple tasks. See the [unified progress bar documentation](5.1 Workflow Engine Progress.md).

**************Version:************** 5.1

  


## workflowRun

Runs a separate workflow.

**************Version:************** 5.1

**Arguments:**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| **url** | string | URL/file of the workflow to run. |   
 |
| elevated | boolean | Whether or not the workflow needs to be ran with elevated permissions. If the workflow does not need to be elevated, it will be ran in the current process. If the workflow does need to be elevated and the current process is not elevated, it will spawn a new elevated instance and run the workflow in that process. _Not supported in UWP._ | false |
| start | string | Task to run after _load_ task has completed. This allows you to use the same workflow JSON for both the elevated and unelevated processes. | start |
| store | string/array | Certificate store used to authenticate (default: "app")Predefined certificate stores:

* app: Application certificate store
* platform: System certificate store
* null: Empty certificate storeIf this value is defined, it forces authenticate to true and requires content to be signed regardless of the protocol used to deliver it. |   
 |
| load | string | Task to run after loading the workflow. This allows you to use the same workflow JSON for both the elevated and unelevated processes. | load |
| unload | string | Task to run before unloading the workflow. This allows you to use the same workflow JSON for both the elevated and unelevated processes. | unload |
| arguments | string/array | Arguments to send to the workflow, if it needs to be elevated. If the value is an array of strings, they are encapsulated by double quotes and combined. |   
 |
| authenticate | boolean | If _true_ it will try to authenticate the signature in the JSON content, _false _otherwise. By default, it will authenticate the JSON on an HTTP connection and will not authenticate the JSON on a HTTPS connection because it is already secure. It will not try to authenticate a connection to the local{ContentUrl}webserver. | true |

**Changes in 5.2:**

* Added store argument

**Status Variables:**

| Name | Type | Description |
|------|------|-------------|
| path | string | Path of the worker application that was launched. |
| arguments | string | Arguments used to launch the worker application. |

**Errors:**

| Name | Description |
|------|-------------|
| Launch_Error_Run | Error occurred while launching process. |
| WorkflowRun_Error_Request | The url request has failed. |
| WorkflowRun_Error_Parse | Failed to parse workflow file. |
| WorkflowRun_Error_Open | Failed to open workflow file. |
| WorkflowRun_Error_Authenticate | Failed to authenticate workflow JSON. |

**Example:**

```
"runElevatedWorkflow":{"type": "workflowRun", "url": "{pathToUrl:{WorkflowDirectory}elevated.json}", "elevated": true, "arguments": "--verbose=25Web* --disablesecurity"}
```

**Example using another task in the same workflow:**

  


```
"runElevatedWorkflow":{"type": "workflowRun", "url": "{ContentUrl}workflow.json", "start": "alternativeStartTask", "elevated": true}
```

  
