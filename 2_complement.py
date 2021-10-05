import sys, csv
import logging

def twocomplement(logger, hostName):
    try:
        logger.debug("Entering twocomplement")
        number = hostName.split(" ")[1][1:]

        number = number[:-1]
        if number is not None:
            if int(number) < 0:
                return hex((1 << 64) + int(number))
            elif int(number) > 0:
                return hex(int(number))
        else:
            return 0

    except Exception as e:
        logger.exception("Encountered exception in twocomplement", e)
    finally:
        logger.debug("Execution completed for twocomplement")

def read_file(logger, filename):
    try:
        new_file_line = "Tenant UUID,Hour,Usage Type,Value,Host Name,Host Units\n"
        logger.debug("Entering read_file")
        with open(filename,"r", encoding='utf-8-sig') as csvfile:
            reader=csv.DictReader(csvfile)
            for row in reader:
                try:
                    if row['Host Name'] is " ":
                        new_file_line = new_file_line + row['Tenant UUID'] + "," + row['Hour'] + "," + row['Usage Type'] + "," + row['Value'] + "," + row['Host Name'] + "," + row ['Host Units'] + "\n"
                        continue

                    hostName = row['Host Name']
                    converted_hostName = (twocomplement(logger, hostName)).upper()
                    new_file_line = new_file_line + row['Tenant UUID'] + "," + row['Hour'] + "," + row['Usage Type'] + "," + row['Value'] + "," + converted_hostName[2:] + "," + row ['Host Units'] + "\n"
                except KeyError as key:
                    print("Got the following KeyError", key)

    except Exception as e:
        logger.exception("Encountered exception in read_file", e)
    finally:
        f = open("ANZ_Australia_HUH_Converted.csv","w")
        f.write(new_file_line)
        f.close()
        logger.debug("Execution completed for read_file")

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print ("No argument is passed. Please pass the csv file that you wish to be converted")
        exit(1)
    else:
        filename = sys.argv[1]

    logging.basicConfig(filename='log_file.txt',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)
    logger = logging.getLogger()
    read_file(logger, filename)
