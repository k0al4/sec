Author: Denis Lima e Alves, PhD
Developed in: Python 3.7, macOS, iPython

The SEC Edgar system (Securities and Exchange Comission Electronic Data Gathering, Analysis and Retrieval)
is a huge source of information regarding information from companies that, for some reason, are required to 
disclose them to their shareholders and general public. This happens through the publication of forms
generally named "filings" and they are several. The most common among them are the 10-K, 10-Q, 8-K and 
DEF 14A and they are filed when some specific event happens and the company has to make that information 
available. For instance, the 10-Ks bring audited financial statement and are disclosed one every year.

Many times, researchers like myself don't have access to most of the mainstream paid databases. However,
much of the data they sell comes from the SEC Edgar system and there is no reason why we couldn't do the
same.

This script is part of my initiative to get all data I need for my research from "free" sources, that is,
where we do not need to pay a subscription to get access. It uses the modules edgar, requests and 
beautifulsoup to access, connect and parse the pages. The requests are done in a way that it is very 
unlikely that they will be denied by the SEC systems. Therefore, there are no treatment for exceptions.

Probably, the most obvious application of this package is to generate a file like the file test1.csv,
available in this repository as an illustration. The variables' descriptions are available in the function
get_metaData's docstring. Just type get_metaData?? (after importing the package, of course) you will see
the documentation. You can do it for all functions in this package, for additional details regarding their
use.

Hence, With this first part, you will be able to download some data from SEC's 10-K filings, such as SIC 
codes and description, IRS number, company's addresses, reporting date and state of incorporation and 
location. This is the information needed to carry on one of my projects in empirical accounting and tax 
research. In the next days, more information will be available to download from financial statements 
using XBRL.

The basic usage is as follows.

The function get_indices downloads the addresses from SEC Edgar. You need to suply the destination folder
where the files (.tsv) will be placed and the starting year. After those are downloaded, the function
write_edgarIndex creates a csv file with the filtered information needed for the download of data. This is
the one similar to the test1.csv file available in this repository as example. The output will consist of a 
bigger csv file with the filing type you need, but only those reported in the year you supplied to this 
function. This file can be used in many other applications, however. You need to supply the arguments as well.

To check which information you need to give each function, type: "function"??

If you have any questions, contact ufudenis@gmail.com
