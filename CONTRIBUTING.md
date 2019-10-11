# How to contribute
First of all thank you for reading this, and wanting to contribute to this little project I started.
I hope this will serve as a nice guide for contribution. It will be updated when needed.

## Reporting bugs and issues
* Check if the issue you want to report does not already exist in the [issue list](https://github.com/Freyj/Fluffy-Hero-Maker/issues). Bugs can be found by searching for the [bug label](https://github.com/Freyj/Fluffy-Hero-Maker/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+label%3Abug). 
* If you want to report a bug please use the [bug report model](https://github.com/Freyj/Fluffy-Hero-Maker/issues/new?assignees=&labels=bug%2C+to+check&template=bug_report.md&title=%5Bbug%5D) with as much information as you can.

## Suggesting enhancements and features
* To suggest new features you can use the [feature request model](https://github.com/Freyj/Fluffy-Hero-Maker/issues/new?assignees=&labels=to+check&template=feature_request.md&title=%5Bfeature+request%5D+Idea).

## Working on existing issues
* If the issue is not assigned, there is most likely no one currently working on it, don't hesitate to drop a comment in the issue to state that you would like to work on it or for any questions you might have regarding the issue.
* Fork the repository, do your magic!
* Once you've solved the issue and everything works fine (as it should :D), do a pull-request on the master
* The pull request will then be reviewed (it should also pass our CI, which uses [Travis CI](https://travis-ci.org) and the [pytest](https://pytest.org/en/latest/) framework.
* Once all is good, we will merge your pull-request by squashing it into one commit into the master branch and close the issue.

##### Commit message standard
* A commit should have a self explanatory title and the rest of the lines should be separated by an empty line and stop at 80 characters.
* Add all the information you think is important on what changed/was added.

##### Coding conventions
This software uses python 3.7 and the requirements are contained in the `requirements.py` file. 
* We aim to follow PEP8 Coding conventions.
* Variable and function names should be clear about their purpose.
* Files and packages should be named by using underscores `package_name_example`.
* Comments and docstrings are important, think about those who will read the code later.

Some of these conventions are not followed by current state of the project and will be corrected in a future update.