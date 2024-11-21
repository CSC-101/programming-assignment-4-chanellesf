from logging import raiseExceptions

import county_demographics
import build_data
import sys
import data

full_data = build_data.get_data()


# PART 1
# Returns the total 2014 Population from the given countries in the provided list
# INPUT: list of CountyDemographics objects
# OUTPUT: integer representing the population sum
def population_list(counties : list[data.CountyDemographics]) -> int:
    x = [county.population['2014 Population'] for county in counties]
    return sum(x)

# PART 2
# Returns a list of given county demographics objects within the specified state
# INPUT: list of County Demographics objects, two-letter state abbreviation str
# OUTPUT: list of County Demographic objects within the specified state
def filter_by_state(counties : list[data.CountyDemographics], text : str) -> list[data.CountyDemographics]:
    return [county for county in counties if county.state == text]

# PART 3
# Returns the total 2014 sub-population across the set of counties in the specified education key
# INPUT: list of County Demographic Objects, education key of interest
# OUTPUT: float repr total sub-population in the specified key of interest based on given counties
def population_by_education(counties : list[data.CountyDemographics], edu : str) -> float:
    x = [(county.education[edu]/100)*county.population['2014 Population'] for county in counties if edu in county.education]
    return sum(x)

# Returns the total 2014 sub-population across the set of counties in the specified ethnicity key
# INPUT: list of County Demographic Objects, ethnicity key of interest
# OUTPUT: float repr total sub-population in the specified key of interest based on given counties
def population_by_ethnicity(counties : list[data.CountyDemographics], eth : str) -> float:
    x = [(county.ethnicities[eth]/100)*county.population['2014 Population'] for county in counties if eth in county.ethnicities]
    return sum(x)

# Returns the total 2014 sub-population across the set of counties that are below poverty
# INPUT: list of County Demographic Objects
# OUTPUT: float repr total sub-population in the specified key of interest based on given counties
def population_below_poverty_level(counties : list[data.CountyDemographics]) -> float:
    x = [(county.income['Persons Below Poverty Level']/100)*county.population['2014 Population'] for county in counties]
    return sum(x)

# PART 4
# Returns the percentage of the total population across the set of counties that are in the specified education key
# INPUT: list of County Demographic Objects, education key of interest
# OUTPUT: float repr total sub-population in the specified key of interest based on given counties
def percent_by_education(counties : list[data.CountyDemographics], edu : str) -> float:
    return round((population_by_education(counties,edu)/population_list(counties))*100,2)

# Returns the percentage of the total population across the set of counties that are in the specified ethnicity key
# INPUT: list of County Demographic Objects, ethnicity key of interest
# OUTPUT: float repr total sub-population in the specified key of interest based on given counties
def percent_by_ethnicity(counties : list[data.CountyDemographics], eth : str) -> float:
    return round((population_by_ethnicity(counties,eth)/population_list(counties)) * 100,2)

# Returns the percentage of the total population across the set of counties that are below poverty level
# INPUT: list of County Demographic Objects
# OUTPUT: float repr total sub-population in the specified key of interest based on given counties
def percent_below_poverty_level(counties : list[data.CountyDemographics]) -> float:
    return round((population_below_poverty_level(counties)/population_list(counties)) * 100,2)

# PART 5
# Returns a list of counties whose specified education key value is greater than the given threshold
# INPUT: list of County Demographic objects, str of the education key of interest, float of the threshold value
# OUTPUT: list of County Demographic objects representing counties greater than the given threshold
def education_greater_than(counties : list[data.CountyDemographics], edu : str, threshold : float) -> list[data.CountyDemographics]:
    return [county for county in counties if edu in county.education and county.education[edu] > threshold]

# Returns a list of counties whose specified education key value is less than the given threshold
# INPUT: list of County Demographic objects, str of the education key of interest, float of the threshold value
# OUTPUT: list of County Demographic objects representing counties greater than the given threshold
def education_less_than(counties : list[data.CountyDemographics], edu : str, threshold : float) -> list[data.CountyDemographics]:
    return [county for county in counties if edu in county.education and county.education[edu] < threshold]

# Returns a list of counties whose specified ethnicity key value is greater than the given threshold
# INPUT: list of County Demographic objects, str of the ethnicity key of interest, float of the threshold value
# OUTPUT: list of County Demographic objects representing counties greater than the given threshold
def ethnicity_greater_than(counties : list[data.CountyDemographics], eth : str, threshold : float) -> list[data.CountyDemographics]:
    return [county for county in counties if eth in county.ethnicities and county.ethnicities[eth] > threshold]

# Returns a list of counties whose specified ethnicity key value is less than the given threshold
# INPUT: list of County Demographic objects, str of the ethnicity key of interest, float of the threshold value
# OUTPUT: list of County Demographic objects representing counties greater than the given threshold
def ethnicity_less_than(counties : list[data.CountyDemographics], eth : str, threshold : float) -> list[data.CountyDemographics]:
    return [county for county in counties if eth in county.ethnicities and county.ethnicities[eth] < threshold]

# Returns a list of counties whose population below poverty level is greater than the given threshold
# INPUT: list of County Demographic objects, float of the threshold value
# OUTPUT: list of County Demographic objects representing counties greater than the given threshold
def below_poverty_level_greater_than(counties : list[data.CountyDemographics], threshold : float) -> list[data.CountyDemographics]:
    return [county for county in counties if county.income['Persons Below Poverty Level'] > threshold]

# Returns a list of counties whose population below poverty level is less than the given threshold
# INPUT: list of County Demographic objects, float of the threshold value
# OUTPUT: list of County Demographic objects representing counties greater than the given threshold
def below_poverty_level_less_than(counties : list[data.CountyDemographics], threshold : float) -> list[data.CountyDemographics]:
    return [county for county in counties if county.income['Persons Below Poverty Level'] < threshold]


def run_operations(stats : list[data.CountyDemographics], line : str,operation: str,measure : str, key : str) -> None:
    try:
        if operation == "population-total":
            print("2014 Population:", population_list(stats))
        elif operation == 'population:':
            # print("pop yuhh")
            if "Ethnicities" in line:
                print("2014", measure, key, ": ", population_by_ethnicity(stats, key))
            elif "Education" in line:
                print("2014", measure, key, ": ", population_by_education(stats, key))
            elif key == "Persons Below Poverty Level":
                print("2014", measure, key, ": ", population_below_poverty_level(stats))
        elif operation == 'percent:':
            # print("percent yuhh")
            if "Ethnicities" in line:
                print("2014", measure, key, ": ", percent_by_ethnicity(stats, key))
            elif "Education" in line:
                print("2014", measure, key, ": ", percent_by_education(stats, key))
            elif key == "Persons Below Poverty Level":
                print("2014", measure, key, ": ", percent_below_poverty_level(stats))
        """
        elif operation == "display":
            for county in stats:
                print("[",county.county,"]")
                print("\tPOPULATION:",county.population['2014 Population'])
                print ("\tAGE")
                for age in county.age:
                    print("\t\t",age,":",county.age[age],"%")
                print("\tEDUCATION")
                for edu in county.education:
                    print("\t\t", edu, ":", county.education[edu], "%")
                print("\tETHNICITIES")
                for eth in county.ethnicities:
                    print("\t\t", eth,":", county.ethnicities[eth],"%")
                print("\tINCOME")
                for income in county.income:
                    if income == 'Persons Below Poverty Level':
                        print("\t\t", income, ":", county.income[income],"%")
                    else: print("\t\t", income, ":", county.income[income])
        """
    except:
        print("Error occurred: Invalid Operation. (@ line {})".format(count))

def main():
    file = "inputs/"+sys.argv[1]
    #infile = open(file, 'r')
    #file_contents = infile.read()
    print(file)

    with open(file, 'r') as infile:

        print(len(full_data), "records loaded.")

        operations = ["population-total", "population:", "percent:", "display", "gt:", "lt:", "filter-state"]
        first_line = infile.readline()
        stats = full_data

        if "filter-state" in first_line:
            state = first_line[first_line.find(":") + 1:].strip()
            print(state)
            stats = filter_by_state(full_data, state)
            print("[FILTER] State -> {} (Entries: {})".format(state, len(stats)))

        infile.seek(0)
        count = 0
        for line in infile:
            count +=1
            try:
                if "filter" in line:
                    if "filter-state" in first_line:
                        stats = filter_by_state(full_data,state)
                    else:
                        stats = full_data
                        first_colon_index = line.find(":") + 1
                        criteria = line[line.find("-") + 1:first_colon_index]
                        threshold = float(line[line.find(":", first_colon_index) + 1:].strip())
                        measure = line[line.find(":") + 1:line.find(".")]
                        key = line[line.find(".") + 1:line.find(":", first_colon_index)].strip()

                        if criteria == "gt:":
                            if "Ethnicities" in line:
                                stats = ethnicity_greater_than(stats, key, threshold)
                            elif "Education" in line:
                                stats = education_greater_than(stats, key, threshold)
                            elif key == "Persons Below Poverty Level":
                                stats = below_poverty_level_greater_than(stats, threshold)
                        elif criteria == "lt:":
                            if "Ethnicities" in line:
                                stats = ethnicity_less_than(stats, key, threshold)
                            elif "Education" in line:
                                stats = education_less_than(stats, key, threshold)
                            elif key == "Persons Below Poverty Level":
                                stats = below_poverty_level_less_than(stats, threshold)
                        print("[FILTER] {} -> {}, {} {} ({} entries)".format(measure, key, criteria, threshold, len(stats)))

                if ":" not in line:
                    operation = line.strip()
                elif "-" not in line:
                    operation = line[:line.find(":")+1]
                    measure = line[line.find(":")+1:line.find(".")]
                    key = line[line.find(".")+1:].strip()

                run_operations(stats, line, operation, measure, key)
                #print("measure: ", measure)
            except:
                print("An Error occurred. (@ line {})".format(count))

if __name__ == '__main__':
    try:
        main()
    except:
        print("ERROR: File not found.")
