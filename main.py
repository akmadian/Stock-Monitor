"""
-----Top Level Docstring------
    Created
    May 9th, 2017 12:36PM

------------------------------

    If DRY is violated, there will be an explanation of the violation
    in the class's docstring.

    Current status definitions for DRY Violation documentation.
    - NOBUG - Problem is known, but will not be adressed due to design
              problems or domain limitations. - SEE PEP-350 Code Tags
    - MAYFIX - Problem is known, will fix if possible.
"""
# IDEA:Implement kwargs in all functions and classes
# IDEA:Implement error handling
# IDEA:Look in to __repr__ implementation
# TODO: Implement configparser support for private information
# TODO: Check to see if docstrings are up to date
# TODO: See if plotting mpl plots with a function is possible
# TODO: See if implementation of commonly used functions across all programs as a module is possible
# TODO: Implement exception handling for handling of blank config file fields
# TODO: Implement request exception handling from Machine-Learning COMMODITIES_GOLD.py

import numpy as np		         # Num processing
import matplotlib.pyplot as plt  # Graphing and tables
from lxml import html            # HTML Scraping
import requests                  # Gets HTML
import time as time              # Time
import csv                       # CSV Parsing
import sys, traceback            # Exception handling
import random
import smtplib                   # Email
from string import Template      # Email text formatting
from twilio.rest import Client
import configparser


twilio_acc_sid = None
twilio_auth_token = None
client = Client(twilio_acc_sid, twilio_auth_token)


site = 'https://www.investing.com/commodities/real-time-futures'
header = {'User-Agent': 'Mozilla/5.0'}
_xpaths_csv_keys = ('Last', 'High', 'Low', 'Chg.', 'Chg. %', 'Time', 'T?')
private_stuff_keys = ('LAR_email_email', 'LAR_email_password', 'twilio_acc_sid',
                      'twilio_auth_token', 'twilio_send_num', 'twilio_receive_num')
silver_values = []
copper_values = []
aluminum_values = []
gold_values = []
data = []
pbt_data = []
gold_last_5 = [1.0, 1.0, 1.0, 1.0, 1.0]
silver_last_5 = [1.0, 1.0, 1.0, 1.0, 1.0]


class LAR:
    """LAR stands for logging and reporting. These functions generate error
            reports and emails them to the email address defined.
    DESCTIPTIONS-
    gather_data - takes information provided in the except clause that
                  called it and puts it all together in a dictionary
                  which can be passed to csvops or a text file for
                  local logging or emailed for offsite logging.
    email_report - generates an email with a template and the dictionary
                   made in gather_data.
                 - Note - The long multiline string defined as t violates
                          PEP-8 and decreases readability in code in favor
                          of better formatting and readability in the email
                          log. Indentation levels are neccessary.
    """
    @staticmethod
    def gather_data(**kwargs):
        print(kwargs)
        d1 = {'time': scrape.get_time()}
        ex_data = {**d1, **kwargs}
        LAR.email_report(ex_data, LAR.file_logging(ex_data))

    @staticmethod
    def email_report(args, was_locallog_succ):
        print(args)
        lls = str(was_locallog_succ)
        try:
            stuff = csvops.csv_read('private_stuff', private_stuff_keys)
            print(stuff)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(str(stuff[0]), str(stuff[1]))
            t = Template("""Program name.......: Stock Monitor
Time of exception..: $time
Exception Type.....: $exType
Callback message...:
$message






Custom Handle......: $custHandle

Additional info....: $addInfo



""")
            mes = 'Subject: Exception occured and was caught\n\n' + t.substitute(args) + \
                  'Local Log Code.: ' + lls + '\n\n End exception log'
            server.sendmail(str(stuff[0]), 'TO_EMAIL', mes)
            server.quit()
        except RuntimeError:
            print('No connection made')
            exit()

    @staticmethod
    def text_report():  # TODO
        pass

    @staticmethod
    def file_logging(args):  # TODOC
        count = 0
        fname = str(''.join(['log_', str(scrape.get_time_for_log()), '.txt']))
        with open(fname, 'w') as repfile:
            for key in args:
                count += 1
                repfile.write(str(key) + ' ....: ' + str(args[key]) + '\n')
        return True


# Class with csv operations
class csvops:
    """CSV file operations
    DESCRIPTIONS-
    csv_write - Writes data to a CSV file
    csv_read - Reads data from a CSV file and returns it

    ARGS-
    csv_write - 'file' is the name of the file to be written to without the
                       extension.
                'content' expects a dictionary, the keys of which will be
                          the headers, and the values will be the
                          corresponding values.

    csv_read -  'file' is the name of the file to be read from without the
                       extension.
                 'content' expects a list with the key names of the values
                           you wish to retrieve.
    """

    @staticmethod
    def csv_write(file, content):
        comblist = [str(file), '.csv']
        filename = str(''.join(comblist))
        with open(filename, 'w') as csvfile:
            fieldnames = _xpaths_csv_keys  # TODO add code to dynamically take dict keys
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(content)

    @staticmethod
    def csv_read(file, content):
        out = []
        comblist = [str(file), '.csv']
        filename = str(''.join(comblist))
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                for key in content:
                    value = row[str(key)]
                    out.append(value)
            return out


# Scrape operations class
class scrape:
    """The scrape class uses HTML scraping to get stock values from a website.
    DESCRIPTIONS-
    scrape - Gets the stocks page, scrapes the values, and does some string
             formatting to make the values readable, and writes them to a
             list.
           - Note - There is a warning about a variable possibly being
                    referenced before assignment (joinedvalue) in scrape
                    in the last Logic section, warning is known, warning
                    does not trigger an exception.
                    Current Status - NOBUG
           - Note - The long, multiline string is used for error message logging.
                    Does not follow PEP-8 and sacrifices readability in favor of
                    message formatting in error log.

    write_data - Gets the XPaths for each value for each element, calls scrape
                 to get the data, then does some list modifications and
                 formatting to get the data ready for display in the table.
    get_time - Gets the current time, selects indicies from the return of
               time.localtime(), does some string formatting, and returns the
               formatted list.
    istrading - Determines if a certain element is trading or not by calling
                get_time, and comparing system time to trading hours for
                each element. Returns bool.

    ARGS-
    scrape - 'xpath' is the xpath of the value to be retrieved.
             'ele' expects a string with the name of the element that is
                   being scraped. Used to update progress bar and create
                   data structure for mpl.
    istrading - 'ele' is the element that will be referenced for wheter
                      it is trading or not.

    DRY VIOLATIONS-
    in write_data() - Logic Sections: 2, 3, 4, 5 - Data manipulation,
                      list calls differ, and differences can not be
                      accounted for with a function parameter.
                      Current status - MAYFIX

    """

    @staticmethod
    def scrape(xpath, ele):  # TODO:Add xpath iterator for multi value return
        str(xpath)
        value_ = []
        #page = requests.get(site)
        #code = str(page.status_code)
        code = '403'
        try:
            assert (code != '403')
        except AssertionError:
            custHand = 'Bad status code returned: %s' % code
            exc_type, exc_value, exc_traceback = sys.exc_info()
            exc_mes = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
            addin = """ AssertionError occurred during status code check.
See scrape.scrape in Stockmonitor/main.py
This exception means that a bad status code was returned during the get request of the stock site."""
            LAR.gather_data(exType='AssertionError', message=exc_mes, custHandle=custHand, addInfo=addin)
        else:
            tree = html.fromstring(page.content)
            notconverted = tree.xpath(xpath)
            semiconverted = notconverted[0].text
            converted = str(semiconverted.encode('utf-8'))
            for letter in converted:
                conditional = bool(letter.isdigit() or letter == '.' or
                                   letter == ',' or letter == '+' or
                                   letter == '-' or letter == '%')
                if conditional:
                    value_.append(letter)
                    joinedvalue = ''.join(value_)
                elif (conditional is False) or (letter == 'b'):
                    pass
            if ele == 'gold':
                gold_values.append(joinedvalue)
            elif ele == 'silver':
                silver_values.append(joinedvalue)
            elif ele == 'aluminum':
                aluminum_values.append(joinedvalue)
            else:
                copper_values.append(joinedvalue)

    @staticmethod
    def write_data():
        count = 0
        prog_dict = {1: '-      | 1/7',
                     2: '--     | 2/7',
                     3: '---    | 3/7',
                     4: '----   | 4/7',
                     5: '-----  | 5/7',
                     6: '------ | 6/7',
                     7: '-------| 7/7' + '\n'}
        gold_xpaths = csvops.csv_read('gold_xpaths', _xpaths_csv_keys)
        silver_xpaths = csvops.csv_read('silver_xpaths', _xpaths_csv_keys)
        copper_xpaths = csvops.csv_read('copper_xpaths', _xpaths_csv_keys)
        aluminum_xpaths = csvops.csv_read('aluminum_xpaths', _xpaths_csv_keys)

        for index_ in gold_xpaths:
            scrape.scrape(index_, 'gold')  # Get the value for each XPath
            count += 1
            sys.stdout.write('\r' + 'Gold     |' + prog_dict[count])  # Update progress bar
            sys.stdout.flush()
            if len(pbt_data) == 1:  # Update progress bar in plot
                del pbt_data[0]
                pbt_data.append('\r' + '|' + prog_dict[count])
        gold_values[5] = scrape.get_time()  # Change time value to readable time
        gold_values[6] = scrape.istrading('gold')  # Change is trading to bool
        data.append(gold_values)
        value_g = gold_values[0]  # Manipulate list
        del gold_last_5[0]
        value_g_ = float(value_g.replace(',', ''))
        gold_last_5.append(value_g_)
        count = 0

        for index_ in silver_xpaths:
            scrape.scrape(index_, 'silver')
            count += 1
            sys.stdout.write('\r' + 'Silver   |' + prog_dict[count])
            sys.stdout.flush()
        silver_values[5] = scrape.get_time()
        silver_values[6] = scrape.istrading('silver')
        data.append(silver_values)
        value_s = silver_values[0]
        del silver_last_5[0]
        value_s_ = float(value_s.replace(',', ''))
        silver_last_5.append(value_s_)
        count = 0

        for index_ in copper_xpaths:
            scrape.scrape(index_, 'copper')
            count += 1
            sys.stdout.write('\r' + 'Copper   |' + prog_dict[count])
            sys.stdout.flush()
        copper_values[5] = scrape.get_time()
        data.append(copper_values)
        count = 0

        for index_ in aluminum_xpaths:
            scrape.scrape(index_, 'aluminum')
            count += 1
            sys.stdout.write('\r' + 'Aluminum |' + prog_dict[count])
            sys.stdout.flush()
        aluminum_values[5] = scrape.get_time()
        data.append(aluminum_values)

    @staticmethod
    def get_time():
        timelist = list(time.localtime())
        time_ = [str((timelist[3])), str(timelist[4]), str(timelist[5])]
        if len(time_[2]) == 1:
            L = [time_[2], '0']
            time_[2] = str(''.join(L))
        if len(time_[1]) == 1:
            L_ = ['0', time_[1]]
            time_[1] = str(''.join(L_))
        time__ = ':'.join(time_)
        return time__

    @staticmethod
    def get_time_for_log():
        timelist = list(time.localtime())
        time_ = [str((timelist[3])), str(timelist[4]), str(timelist[5])]
        if len(time_[2]) == 1:
            L = [time_[2], '0']
            time_[2] = str(''.join(L))
        if len(time_[1]) == 1:
            L_ = ['0', time_[1]]
            time_[1] = str(''.join(L_))
        time__ = '-'.join(time_)
        return time__

    @staticmethod
    def istrading(ele):
        timelist = list(time.localtime())
        time_ = [timelist[3], str(timelist[4]), str(timelist[5])]
        if ele != 'aluminum' and (15 < time_[0] or time_[0] < 14):
            return 'True'
        else:
            return 'False'


# Matplotlib code
class mpl:
    # TODO:Add code to dynamically adjust y axis limits for low values.
    """ Uses matplotlib to make data visualizations
    DESCRIPTIONS-
    initialize_gui - Initializes the gui, includes figure, and all plots.

    update - Updates the currently shown plots with new data.
           - Note - The top level if statement in update() is needed because
                    the way the plots are removed and redrawn is dependent
                    on a small syntactical difference.
                    ex. p1.remove() is needed first because of the way the
                                    subplots from initialize_gui() are handled
                        ax1.remove() is needed second because the plots
                                     created in initialize_gui() are no
                                     longer being handled.
                    I know, it looks terrible and is super inefficient
                    and is a terrible violation of DRY, this whole
                    honkin class is. It's painful for me too. Code gods,
                    please allow for mercy = True.
    ARGS-
    update - 'p1, p2, p3, p4' - All very similar in what they take -
                                the name of the plot from initialize_gui()
                                only used when first_run is True.
                                See update - Note for more info on why
                                they're necessary.

    DRY VIOLATIONS-
    in initialize_gui - Logic Sections: * - matplotlib is very line
                        intensive, many lines are necessary to build
                        plots.
                        Current Status - NOBUG
    in update - Logic Sections: * - see above DRY Violation explanation
                SEE NOTE IN DESCRIPTIONS - update FOR HORRIBLY PAINFUL
                DRY VIOLATION, AGAIN, IM SO SORRY IF YOU HAVE TO LOOK
                AT THAT.
                Current Status - MAYFIX
    """
    update_count = 0
    first_run = True
    columns = ('Last', 'High', 'Low', 'Chg.', 'Chg. %', 'Time', 'T?')
    rows = ['Gold', 'Silver', 'Copper', 'Aluminum']

    @staticmethod
    def initialize_gui():
        scatter_x = (1, 2, 3, 4, 5)
        fig = plt.figure(figsize=(8, 8))
        ax1 = plt.subplot2grid((11, 3), (0, 0), rowspan=2, colspan=2)
        ax2 = plt.subplot2grid((11, 3), (2, 0), rowspan=3, colspan=2)
        ax3 = plt.subplot2grid((11, 3), (5, 0), rowspan=3, colspan=2)
        ax4 = plt.subplot2grid((11, 3), (8, 0), rowspan=3, colspan=2)
        # ax5 = plt.subplot2grid((11, 3), (0, 3), rowspan=2) TODO
        plt.ion()

        # Table - Main table
        ax1.axis('tight')
        ax1.axis('off')
        ax1.set_title('Data')
        ax1.table(cellText=data,
                  rowLabels=mpl.rows,
                  colLabels=mpl.columns,
                  loc='center')

        # Gold last graph
        largestx = ()
        largesty = ()
        annpoint = ()
        anntext = ()
        largest = 1
        gold_last_ = ''
        for index in gold_last_5:
            if (index > largest) or (index == largest):
                largest = index
                largesty = ((index + 0.5), (index - 0.5))
                largestx = ((gold_last_5.index(index) + 1),
                            (gold_last_5.index(index) + 1))
                annpoint = ((gold_last_5.index(index) + 1.0), index)
                anntext = ((gold_last_5.index(index) + 1.05), (index + 0.5))
                gold_last_ = '[' + str(largest) + ']' + '\n' + 'Highest Last'
                if (gold_last_5.index(index) + 1) > 4.55:
                    anntext = ((gold_last_5.index(index) - 0.05), (index + 0.5))
        ax2.plot(largestx, largesty)
        ax2.annotate(gold_last_, xy=annpoint, xytext=anntext)
        ax2.scatter(scatter_x, gold_last_5, color='red')
        ax2.plot(scatter_x, gold_last_5, color='red')
        ax2.set_xlim(0.75, 5.25)
        ax2.set_ylim(1248.75, 1263.25)
        ax2.set_yticks(np.linspace(1258.0, 1263.0, 6, endpoint=True))
        ax2.set_ylabel('Gold Last')
        ax2.set_title('Updated [' + str(mpl.update_count) + '] times')

        # Silver last graph
        largestx_ = ()
        largesty_ = ()
        annpoint_ = ()
        anntext_ = ()
        largest_ = 1
        silver_last_ = ''
        try:
            (len(silver_last_5) - 1) < 16.45
        except Exception:
            pass
        for index_ in silver_last_5:
            if (index_ > largest_) or (index_ == largest_):
                largest_ = index_
                largesty_ = ((index_ + 0.04), (index_ - 0.04))
                largestx_ = ((silver_last_5.index(index_) + 1),
                             (silver_last_5.index(index_) + 1))
                annpoint_ = ((silver_last_5.index(index_) + 1.0), index_)
                anntext_ = ((silver_last_5.index(index_) + 1.05), (index_ + 0.04))
                silver_last_ = '[' + str(largest_) + ']' + '\n' + 'Highest Last'
                if (silver_last_5.index(index_) + 1) > 4.55:
                    anntext_ = ((silver_last_5.index(index_) - 0.05), (index_ + 0.04))
        ax3.plot(largestx_, largesty_)
        ax3.annotate(silver_last_, xy=annpoint_, xytext=anntext_)
        ax3.scatter(scatter_x, silver_last_5, color='red')
        ax3.plot(scatter_x, silver_last_5, color='red')
        ax3.set_xlim(0.75, 5.25)
        ax3.set_ylim(16.45, 17.07)
        ax3.set_yticks(np.linspace(16.85, 17.05, 6, endpoint=True))
        ax3.set_xticks(np.linspace(1, 5, 5, endpoint=True))
        ax3.legend(loc='upper left', frameon=False)
        ax3.set_ylabel('Silver Last')

        # Copper last graph
        rint1 = random.randint(1.0, 5.0)
        rint2 = random.randint(1.0, 5.0)
        rint3 = random.randint(1.0, 5.0)
        scatter_y = (0, rint1, rint2, rint3, 5)
        ax4.scatter(scatter_x, scatter_y)
        ax4.set_ylabel('Copper Last')

        # Progress Bar Table TODO
        '''
        ax5.axis('tight')
        ax5.axis('off')
        ax5.set_title('Update Progress')
        ax5.table(cellText=pbt_data,
                  rowLabels=mpl.rows,
                  colLabels='',
                  loc='center')
        '''
        fig.tight_layout()
        mpl.update_count += 1
        plt.pause(0.5)

        while True:
            mpl.update(ax1, ax2, ax3, ax4)
            mpl.update_count += 1

    @staticmethod
    def update(p1, p2, p3, p4):
        scatter_x = (1, 2, 3, 4, 5)
        del data[:]
        del copper_values[:]
        del gold_values[:]
        del aluminum_values[:]
        del silver_values[:]
        scrape.write_data()
        if mpl.first_run:  # NOBUG: See docstring
            p1.remove()
            ax1 = plt.subplot2grid((11, 3), (0, 0), rowspan=2, colspan=2)
            ax1.axis('tight')
            ax1.axis('off')
            ax1.set_title('Data')
            ax1.table(cellText=data,
                      rowLabels=mpl.rows,
                      colLabels=mpl.columns,
                      loc='center')

            p2.remove()
            ax2 = plt.subplot2grid((11, 3), (2, 0), rowspan=3, colspan=2)
            largestx = ()
            largesty = ()
            annpoint = ()
            anntext = ()
            largest = 1
            gold_last_ = ''
            for index in gold_last_5:
                if (index > largest) or (index == largest):
                    largest = index
                    largesty = ((index + 0.5), (index - 0.5))
                    largestx = ((gold_last_5.index(index) + 1),
                                (gold_last_5.index(index) + 1))
                    annpoint = ((gold_last_5.index(index) + 1.0), index)
                    anntext = ((gold_last_5.index(index) + 1.05), (index + 0.5))
                    gold_last_ = '[' + str(largest) + ']' + '\n' + 'Highest Last'
                    if (gold_last_5.index(index) + 1) > 4.55:
                        anntext = ((gold_last_5.index(index) - 0.05), (index + 0.5))
            ax2.plot(largestx, largesty)
            ax2.annotate(gold_last_, xy=annpoint, xytext=anntext)
            ax2.scatter(scatter_x, gold_last_5, color='red')
            ax2.plot(scatter_x, gold_last_5, color='red')
            ax2.set_xlim(0.75, 5.25)
            ax2.set_ylim(1248.75, 1263.25)
            ax2.set_yticks(np.linspace(1258.0, 1263.0, 6, endpoint=True))
            ax2.set_xticks(np.linspace(1, 5, 5, endpoint=True))
            ax2.set_ylabel('Gold Last')
            ax2.set_title('Updated [' + str(mpl.update_count) + '] times')

            p3.remove()
            ax3 = plt.subplot2grid((11, 3), (5, 0), rowspan=3, colspan=2)
            largestx_ = ()
            largesty_ = ()
            annpoint_ = ()
            anntext_ = ()
            largest_ = 1
            silver_last_ = ''
            for index_ in silver_last_5:
                if (index_ > largest_) or (index_ == largest_):
                    largest_ = index_
                    largesty_ = ((index_ + 0.04), (index_ - 0.04))
                    largestx_ = ((silver_last_5.index(index_) + 1),
                                 (silver_last_5.index(index_) + 1))
                    annpoint_ = ((silver_last_5.index(index_) + 1.0), index_)
                    anntext_ = ((silver_last_5.index(index_) + 1.05), (index_ + 0.04))
                    silver_last_ = '[' + str(largest_) + ']' + '\n' + 'Highest Last'
                    if (silver_last_5.index(index_) + 1) > 4.55:
                        anntext_ = ((silver_last_5.index(index_) - 0.05),(index_ + 0.04))
            ax3.plot(largestx_, largesty_)
            ax3.annotate(silver_last_, xy=annpoint_, xytext=anntext_)
            ax3.scatter(scatter_x, silver_last_5, color='red')
            ax3.plot(scatter_x, silver_last_5, color='red')
            ax3.set_xlim(0.75, 5.25)
            ax3.set_ylim(16.45, 17.07)
            ax3.set_yticks(np.linspace(16.85, 17.05, 6, endpoint=True))
            ax3.set_xticks(np.linspace(1, 5, 5, endpoint=True))
            ax3.legend(loc='upper left', frameon=False)
            ax3.set_ylabel('Silver Last')
            plt.pause(0.5)
            ax1.remove()
            ax2.remove()
            ax3.remove()
            mpl.first_run = False
        else:
            ax1 = plt.subplot2grid((11, 3), (0, 0), rowspan=2, colspan=2)
            ax1.axis('tight')
            ax1.axis('off')
            ax1.set_title('Data')
            ax1.table(cellText=data,
                      rowLabels=mpl.rows,
                      colLabels=mpl.columns,
                      loc='center')
            plt.pause(0.5)

            ax2 = plt.subplot2grid((11, 3), (2, 0), rowspan=3, colspan=2)
            largestx = ()
            largesty = ()
            annpoint = ()
            anntext = ()
            largest = 1
            gold_last_str = ''
            for index in gold_last_5:
                if (index > largest) or (index == largest):
                    largest = index
                    largesty = ((index + 0.5), (index - 0.5))
                    largestx = ((gold_last_5.index(index) + 1),
                                (gold_last_5.index(index) + 1))
                    annpoint = ((gold_last_5.index(index) + 1.0), index)
                    anntext = ((gold_last_5.index(index) + 1.05), (index + 0.5))
                    gold_last_str = '[' + str(largest) + ']' + '\n' + 'Highest Last'
                    if (gold_last_5.index(index) + 1) > 4.55:
                        anntext = ((gold_last_5.index(index) - 0.05), (index + 0.5))
            ax2.plot(largestx, largesty)
            ax2.annotate(gold_last_str, xy=annpoint, xytext=anntext)
            ax2.scatter(scatter_x, gold_last_5, color='red')
            ax2.plot(scatter_x, gold_last_5, color='red')
            ax2.set_xlim(0.75, 5.25)
            ax2.set_ylim(1247.75, 1263.25)
            ax2.set_yticks(np.linspace(1258.0, 1263.0, 6, endpoint=True))
            ax2.set_ylabel('Gold Last')
            ax2.set_title('Updated [' + str(mpl.update_count) + '] times')
            plt.pause(0.5)

            ax3 = plt.subplot2grid((11, 3), (5, 0), rowspan=3, colspan=2)
            largestx_ = ()
            largesty_ = ()
            annpoint_ = ()
            anntext_ = ()
            largest_ = 1
            silver_last_ = ''
            for index_ in silver_last_5:
                if (index_ > largest_) or (index_ == largest_):
                    largest_ = index_
                    largesty_ = ((index_ + 0.04), (index_ - 0.04))
                    largestx_ = ((silver_last_5.index(index_) + 1),
                                 (silver_last_5.index(index_) + 1))
                    annpoint_ = ((silver_last_5.index(index_) + 1.0), index_)
                    anntext_ = ((silver_last_5.index(index_) + 1.05), (index_ + 0.04))
                    silver_last_ = '[' + str(largest_) + ']' + '\n' + 'Highest Last'
                    if (silver_last_5.index(index_) + 1) > 4.55:
                        anntext_ = ((silver_last_5.index(index_) - 0.05), (index_ + 0.04))
            ax3.plot(largestx_, largesty_)
            ax3.annotate(silver_last_, xy=annpoint_, xytext=anntext_)
            ax3.scatter(scatter_x, silver_last_5, color='red')
            ax3.plot(scatter_x, silver_last_5, color='red')
            ax3.set_xlim(0.75, 5.25)
            ax3.set_ylim(16.45, 17.07)
            ax3.set_yticks(np.linspace(16.85, 17.05, 6, endpoint=True))
            ax3.set_xticks(np.linspace(1, 5, 5, endpoint=True))
            ax3.legend(loc='upper left', frameon=False)
            ax3.set_ylabel('Silver Last')
            plt.pause(0.5)

    @staticmethod
    def update_progress():  # TODO:Need to work out how to call #TODOC
        ax5 = plt.subplot2grid((11, 3), (0, 3), rowspan=2)
        ax5.axis('tight')
        ax5.axis('off')
        ax5.set_title('Update Progress')
        ax5.table(cellText=pbt_data,
                  loc='center')
        plt.pause(0.5)


scrape.write_data()

print('Gold Values......:' + str(gold_values))
print('Silver Values....:' + str(silver_values))
print('Copper Values....: ' + str(copper_values))
print('Aluminum Values..: ' + str(aluminum_values))
print('Data: ' + str(data))
