import build_data
import sys
import data

full_data = build_data.get_data()
operations = ["DEFAULT","population-total", "population:", "percent:", "display", "gt:", "lt:", "state"]
keys = ["DEFAULT","Bachelor's Degree or Higher", "High School or Higher", "American Indian and Alaska Native Alone",
        "Asian Alone", "Black Alone", "Hispanic or Latino", "Native Hawaiian and Other Pacific Islander Alone",
        "Two or More Races", "White Alone", "White Alone, not Hispanic or Latino", "Persons Below Poverty Level"]
filters = ["state:","lt:","gt:"]

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


def run_operations(stats : list[data.CountyDemographics], line : str) -> None:
    value = 0.0
    operation = "DEFAULT"
    key = "DEFAULT"
    measure = "DEFAULT"

    if ":" not in line:
        operation = line.strip()
    elif "-" not in line:
        operation = line[:line.find(":") + 1]
        measure = line[line.find(":") + 1:line.find(".")]
        key = line[line.find(".") + 1:].strip()

    if operation not in operations or key not in keys:
        raise ValueError("Error: Invalid input.")
    if operation == "population-total":
        print("2014 Population:", population_list(stats))
    elif operation == 'population:':
        # print("pop yuhh")
        if "Ethnicities" in line:
            value = population_by_ethnicity(stats, key)
        elif "Education" in line:
            value = population_by_education(stats, key)
        elif key == "Persons Below Poverty Level":
            value = population_below_poverty_level(stats)
        print("2014", measure, key, ": ", value)
    elif operation == 'percent:':
        # print("percent yuhh")
        if "Ethnicities" in line:
            value = percent_by_ethnicity(stats, key)
        elif "Education" in line:
            value = percent_by_education(stats, key)
        elif key == "Persons Below Poverty Level":
            value = percent_below_poverty_level(stats)
        print("2014", measure, key, ": ", value, "%")
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


def filter_data(stats : list[data.CountyDemographics], line : str) -> list[data.CountyDemographics]:
    first_colon_index = line.find(":") + 1
    filter = line[line.find("-") + 1:first_colon_index]
    new_stats = 0
    if filter not in filters:
        raise ValueError("Error: Invalid input.")

    if filter == "state:":
            state = line[line.find(":") + 1:].strip()
            new_stats = filter_by_state(stats, state)
            print("[FILTER] State -> {} (Entries: {})".format(state, len(new_stats)))
    else:
        threshold = float(line[line.find(":", first_colon_index) + 1:].strip())
        measure = line[line.find(":") + 1:line.find(".")]
        key = line[line.find(".") + 1:line.find(":", first_colon_index)].strip()
        if filter == "gt:":
            if "Ethnicities" in line:
                new_stats = ethnicity_greater_than(stats, key, threshold)
            elif "Education" in line:
                new_stats = education_greater_than(stats, key, threshold)
            elif key == "Persons Below Poverty Level":
                new_stats = below_poverty_level_greater_than(stats, threshold)
        elif filter == "lt:":
            if "Ethnicities" in line:
                new_stats = ethnicity_less_than(stats, key, threshold)
            elif "Education" in line:
                new_stats = education_less_than(stats, key, threshold)
            elif key == "Persons Below Poverty Level":
                new_stats = below_poverty_level_less_than(stats, threshold)
        print("[FILTER] {} -> {}, {} {} ({} entries)".format(measure, key, filter, threshold, len(new_stats)))
    return new_stats

def main():
    file = "inputs/"+sys.argv[1]
    #infile = open(file, 'r')
    #file_contents = infile.read()
    print(file)


    with open(file, 'r') as infile:

        print(len(full_data), "records loaded.")

        stats = full_data

        infile.seek(0)
        count = 0
        for line in infile:
            count +=1
            try:
                if "filter" in line:
                    stats = filter_data(stats,line)
                else:
                    run_operations(stats, line)
            except:
                print("An Error occurred. (@ line {}: {})".format(count,line.strip()))

if __name__ == '__main__':
    try:
        main()
    except:
        print("ERROR: File not found.")
