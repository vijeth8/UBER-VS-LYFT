{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# UBER vs LYFT\n",
    "## Ride Recommendation and Surge analysis "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<img src=\"UBER_LYFT.png\">"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "-------------"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 8 properties for Big Data systems :"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Robustness and fault Tolerance"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    ">Since all the systems used belong to AWS. All systems used for the project neatly integrates with one another, with good Robustness. \n",
    "\n",
    ">All the raw data required is stored in s3. Incase some system fails, the data can still be used to recompute the desired results.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Low latency reads and updates"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Latency is an important issue for my projct. Real time ride recommendation should be fast enough to not bore the user.\n",
    "Using kanesis to store the data in s3 and reading this data off of s3 shouldn't take long.\n",
    "\n",
    "When it comes to the analysis of historical surge data, Latency is not very important. But, using spark cuts down thelatency on general by avoiding unnecessary disk i/o.\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Scalability"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "S3 is good enough to hold huge amount of data."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Generalization"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "This architecture can be reused for a lot of applications. Especially for comparing two online  services"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Extensibility\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Apart from the sysytems that store the raw data, any of the system can be replaced with a better ones if there are any available. or may be for a different application, using the same data.\n",
    "\n",
    "example : Kafka can be used instead of Kenisis. Hadoop can be used instead of spark , if thats appropriate. Hbase or cassandra can be used instead of postgresql."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Ad hoc queries"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "PostgreSQL will be used to do ad hoc queries."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Minimal maintainance"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "As all the components are maintained AWS, there is very less to worry about interms of maintainance.\n",
    "\n",
    "When it comes to scale, the postgresql can be of a problem. This an be replaced with an appropriate rdbms system."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Debuggability"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "I will be having some checkpoints at some stages in my pipeline, to make sure that everything is running as planned. These checkpoints can be like a mail to notify myself the amount/count of data that I have collected.If the RDBMS crashes, there will be a parquet on s3 to fall back on. "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "-----------"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "collapsed": true
   },
   "source": [
    "## How does my system fall short and how can it be improved ?"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "If I have to collect huge data, postgreSQL wouldn't be the right choice. Other tan that I think I have everything I need for my project. I need to work on effectively creating a Web app"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "anaconda-cloud": {},
  "kernelspec": {
   "display_name": "Python [conda env:dsci6007]",
   "language": "python",
   "name": "conda-env-dsci6007-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 2
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython2",
   "version": "2.7.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 1
}
