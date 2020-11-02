# sec
Utilities to work with data from the SEC Edgar


Author: Denis Lima e Alves, PhD
Developed in: Python 3.7, macOS, iPython

This script is part of my initiative to get all data I need for my research from "free" sources, that is,
where we do not need to pay a subscription to get access. It uses edgar, requests and beautifulsoup to
access, connect and parse the pages. The requests are done in a way that it is very unlikely that SEC will 
deny them. Therefore, there are no treatment for exceptions.

With this first part, you will be able to download some data from SEC's 10-K filings, such as SIC codes 
and description, IRS number, company's addresses, reporting date and state of incorporation and location. 
This is the information needed to carry on one of my projects in empirical accounting and tax 
research. In the next days, more information will be available to download from financial statements 
using XBRL.

The basic usage is as follows.

The function get_indices downloads the addresses from SEC Edgar. You need to suply the destination folder
where the files (.tsv) will be placed and the starting year. After those are downloaded, the function
write_edgarIndex creates a csv file with the filtered information needed for the download of data. The
output will consist of a bigger csv file with the filing type you need, but only those reported in the year
you supplied to this function. This file can be used in many other applications, however. You need to supply
the arguments as well.

To check which information you need to give each function, type: "function"??

If you have any questions, contact ufudenis@gmail.com
