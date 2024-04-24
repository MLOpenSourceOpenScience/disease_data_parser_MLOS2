
"""
RTF Extractor

From raw data, extract necessary data and translate
it into RTF format. This includes header, diseases,
dates, and other data as well.

Dependency:
- pip install python-dateutil

Author: MLOS^2_NLP_TEAM
Date: 2024.02.09
"""

from datetime import datetime,timedelta
import re
from typing import List, Tuple, Optional
from dateutil.parser import parse
from disease_header_parser import detect_diseases

def extract_date_components(text: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    '''
    Arguments: string with rtf data
    Returns: string with rtf data relevant for tables,
        2 element array with the start and end timestamp
    '''
    # Regular expression pattern to match the date format
    pattern = r'(?s:.*)\b(\d{1,2})\s*(?:st|nd|rd|th)\s*\w{0,9}\s*[-–—]+\s*(\d{1,2})\s*(?:st|nd|rd|th)?\s*(\w+)\s*(\d{4})?\s*\('
    # \s{0,1}\( on the end?

    # Search for the pattern in the text
    match = re.search(pattern, text)

    if match:
        # Extract day, month, and year from the matched groups
        day = match.group(2)
        month = match.group(3)
        year = match.group(4)

        if year is None and month[-1].isdigit():
            # handles 26th Mar2021
            year = month[-4:]
            month = month[:-4]
        elif year is None:
            # handels 26thMar 2021
            pattern_year = r'(?s:.*)\b(\d{1,2})\s*(?:st|nd|rd|th)\s*\w{0,4}?[-–—]+\s*(\d{1,2})\s*(?:st|nd|rd|th)?\s*(\w+)\s*(\d{4})'
            year_match = re.search(pattern_year, text)

            year = year_match.group(4)

        return day, month, year
    else:
        print("Error: Date not found")
        return None, None, None


#given a start and end word, extract the table between them
def extract_table(first_word: str, end_words: List[str], text: str) -> Optional[str]:
    """
    Find starting word, and second-startinf word from text
    then extract data as a line, starting from found place

    Parameters:
    - first_word (str): First word that want to be found.
    - second_word (str): Second-starting word that want to be found.
    - text (str): Raw data.

    Returns:
    - Optional[str]: Data that is extracted, return None if not found.
    """
    subset = ""
    found_starting_word = False
    temp_diseases = []

    #print("DEBUG: looking for starting word")
    for idx, word in enumerate(text.split()):
        if (found_starting_word and len(subset.split())==4):
            #print("DEBUG: checking validity of next words")
            #print("starting word found: ",subset)
            try:
                #print("DEBUG: checking", subset.split()[1])
                temp_diseases = detect_diseases((subset))
            except ValueError:
                subset = ""
                found_starting_word = False
                #print("DEBUG: non disease detected, start word invalid")
                continue
            if temp_diseases.count("ignore") > 0 or len(temp_diseases) == 0:
                    subset = ""
                    found_starting_word = False
                    #print("DEBUG: non disease detected, start word invalid")
                    continue
        if found_starting_word:
            if word in end_words and len(subset.split())>300:
                #print("DEBUG: end word found:", word)
                break
            subset += word + " "
            #print("DEBUG: adding", word, "to subset")
        elif word == first_word:
            found_starting_word = True
            #print("DEBUG: starting word found")
            subset += word + " "
        elif word in first_word:
            #print("DEBUG: starting word found kinda wack tho")
            found_starting_word = True
            subset += word + " "

    #print("DEBUG: subset", subset)
    return subset.strip()



def extract_data_from_rtf(rtf_data: List[str], manual_mode: bool) -> Tuple[Optional[List[str]],
                                                        Optional[List[datetime]]]:
    
    table = ["",""]
    # months used to convert text month to datetime
    ''' No longer used
    month_dict = {
        'Jan': 1,
        'January': 1,
        'February': 2,
        'Feb': 2,
        'March': 3,
        'Mar': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'Aug': 8,
        'September': 9,
        'Sep': 9,
        'October': 10,
        'Oct': 10,
        'November': 11,
        'Nov': 11,
        'December': 12,
        'Dece": 12,
        'Dec': 12
    }
    '''
    if manual_mode:
        print("manual input mode enabled")
        print("raw text: ", rtf_data[0])

        day = input("Enter the day: ")
        month = input("Enter the month: ")
        year = input("Enter the year: ")

        table[1] = input("Enter the table: ")
        table[0] = table[1]

    else:



        day, month, year = extract_date_components(rtf_data[0])
        if(day is None or month is None or year is None):
            print("Error: Invalid date")
            return None, None

        if __name__ == "__main__":
            # Print the extracted date components
            print("Day:", day)
            print("Month:", month)
            print("Year:", year)

        if month == 'Janu':
        # Exception Handling
            month = 'January'
        elif month == 'Febr':
            month = 'February'
        elif month == 'Marc':
            month = 'March'
        elif month == 'Apri':
            month = 'April'
        elif month == 'May':
            month = 'May'
        elif month == 'June':
            month = 'June'
        elif month == 'July':
            month = 'July'
        elif month == 'Augu':
            month = 'August'
        elif month == 'Sept':
            month = 'September'
        elif month == 'Octo':
            month = 'October'
        elif month == 'Nove':
            month = 'November'
        elif month == 'Dece':
            month = 'December'

        end_date = parse(f"{year} {month} {day}")
        table_change_date = datetime(2013, 5, 17)

        

        if end_date > table_change_date:
            table[0] = extract_table("RDHS", ["Comments", "PRINTING", "WRCD", "Source", "WER", "Table"], rtf_data[0])
            table[1] = extract_table("RDHS", ["Comments", "PRINTING", "WRCD", "Source", "WER", "Table"], rtf_data[1])
        else:
            table[0] = extract_table("DPDHS", ["Comments", "PRINTING", "WRCD", "Source", "WER", "Table"], rtf_data[0])
            table[1] = extract_table("DPDHS", ["Comments", "PRINTING", "WRCD", "Source", "WER", "Table"], rtf_data[1])
            #MIGHT NOT BE ACCURATE!! TEST this eventually

        #print(table)
        #if old (by volume or date or identifying factor do this or that)

        
        #extract table
        

        #Hardcode fix for "T* C** " ending up in table
        if "T* C** " in table[1]:
            table[1] = table[1].replace("T* C** ", "")
        if "T* C** " in table[0]:
            table[0] = table[0].replace("T* C** ", "")

        #print("table", table)
        #print("dates", dates)

    end_date = parse(f"{year} {month} {day}")
    start_date = end_date - timedelta(days=6)
    dates = [start_date, end_date]

    table[0] = table[0].replace(" ", "\n")
    table[1] = table[1].replace(" ", "\n")
    return table, dates












TEST_STRING2 = """                       WEEKLY EPIDEMIOLOGICAL REPORT
                               A publication of the Epidemiology Unit
                        Ministry of Health, Nutrition & Indigenous Medicine
                                       231, de Saram Place, Colombo 01000, Sri Lanka
                           Tele: + 94 11 2695112, Fax: +94 11 2696583, E mail: epidunit@sltnet.lk
                                  Epidemiologist: +94 11 2681548, E mail: chepid@sltnet.lk
                                                Web: http://www.epid.gov.lk


                  Vol. 50 No. 23                                                                       03 rd – 09th June 2023
 SRI LANKA 2023
                                                                      DENGUE

                  Key facts                                                 DEN2, DEN3 and DEN4). Discarded receptacles
                                                                            (plastic containers, tins, cans, coconut shells etc.),
                      Dengue is a viral infection caused by the
                                                                            water storage containers, automobile tyres and ma-
                  dengue virus (DENV), transmitted to humans via
                                                                            chinery parts, building structures (roof gutters etc.),
                  the bite of infected Aedes species mosquitoes.
                                                                            household /institutional appliances (refrigerator trays,

                      Dengue is found in tropical and sub-tropical         flower vases, ornamental ponds) are identified as
                                                                            major mosquito breeding sites. Female mosquitoes
                  regions throughout the world, mostly in urban and
                                                                            lay their eggs on the inner walls of containers with
                  semi-urban areas.
                                                                            water. The entire life cycle of the mosquito lasts 8-10
                      Nearly 100–400 million dengue infections             days at room temperature but may vary with environ-
                  occur each year while over 20,000 dengue-related          mental conditions.
                  deaths occur annually.                                    Dengue is becoming a major health problem which is
                                                                            both global and local, mainly among urban and semi-
                      A person may be infected with dengue up to 4         urban settings. It is now endemic in more than 100
                  times during their lifetime.                              countries in the WHO Regions of Africa, the Ameri-
                      Many Dengue infections are asymptomatic or           cas, the Eastern Mediterranean, South-East Asia and

                  produce mild illness, while occasionally it may           the Western Pacific. Around 70% of the global dis-

                  cause more severe disease or death.                       ease burden is represented by Asia. There are around
                                                                            3.9 billion of people are at risk of infection with den-
                      Although there is no specific treatment for          gue viruses worldwide. The global incidence of den-
                  dengue, early detection and access to proper              gue infections per year may range between 100 mil-
                  management may significantly lower the risk of            lion and 200 million. Recent estimates identified with
                  death.                                                    cartographic approaches revealed this number is
                                                                            closer to almost 400 million and over 20,000 dengue-
                  Prevention and control of dengue mainly depend
                  on mosquito control.                                      related deaths occur annually.
                                                                            Although clinical dengue-like illness has been report-
WER


                  INTRODUCTION                                              ed in Sri Lanka since the early 20th century
                                                                            (serologically confirmed in 1962), Dengue fever and
                  Dengue is a viral infection transmitted by the bite of
                                                                            Dengue Haemorrhagic fever became nationally notifi-
                  an infected Aedes type of mosquito primarily the Ae-
                                                                            able diseases in Sri Lanka in 1996. Dengue shows a
                  des aegypti mosquito. Once infectious, the mosquito
                                                                            seasonal transmission in Sri Lanka with two peaks
                  can transmit the virus for the rest of its life. Though
                                                                            occurring with the monsoon rains in June to July and
                  this mosquito originated in Africa, it is now found
                                                                            October to December respectively while the majority
                  in tropical, subtropical and temperate regions through-
                                                                            of cases occur during June to July.
                  out the world. Although there are around 140 species
                  of mosquitoes could be found in Sri Lanka, only Ae-       There was an island-wide epidemic of dengue with 51
                  des aegypti and Aedes albopictus mosquitoes trans-        cases of DHF and 15 deaths during the period 1965-
                  mit the dengue virus to humans. There are four sero-      1968. Thereafter, from the early 1990s, progressively
                  types of the virus which can cause dengue (DEN1,


                      Contents                                                                                             Page
                      1. DENGUE                                                                                            1
                      2. Summary of selected notifiable diseases reported (27th – 02nd June 2023)                          3
                      3. Surveillance of vaccine preventable diseases & AFP (27th – 02nd June 2023)                        4
WER Sri Lanka - Vol. 50 No . 23                                                                                         03rd– 09th June 2023

large epidemics with more severe and fatal DHF were reported at reg-        can be treated at home with pain medicine while for people with severe
ular intervals. There were two epidemics of dengue reported in 2002         dengue, hospitalization is often needed. There is no specific treatment
and 2004 with 8931 cases and 15463 cases respectively. In 2017, a           for dengue. Acetaminophen (paracetamol) can be used to control pain
total of 186 101 suspected dengue cases and 440 dengue-related              while Nonnon-steroidal anti-inflammatory drugs like ibuprofen and
deaths were reported to the Epidemiology Unit which is the highest          aspirin should be avoided as they may increase the risk of bleeding.
number of suspected cases reported in a single calendar year in Sri         There is a novel vaccine called Dengvaxia for people who have had
Lanka since 1996.                                                           dengue at least once in their lives and live in places where the disease
                                                                            is more common. Patients who are being managed at home must first
In 2019, the mid-year peak in reported cases was shifted to the latter
                                                                            contact doctors and should also ensure adequate oral fluid intake to
half of the year and this trend continued into early 2020 with a total of
                                                                            maintain normal urine output.
11 607 cases reported in January 2020 which was higher than the
reported cases for the same period during 2017. Thereafter the report-      Prevention
ed number of dengue cases during April- June 2020 dropped below             There are no vaccines or specific antiviral therapies currently existing
the past five-year national average. This could be due to population-       to control the growing threat of dengue globally. Early case detection
wide mobility restrictions imposed as a response to the COVID-19            and appropriate clinical management can reduce mortality. Effective
pandemic and people were encouraged to stay at home and work from           mosquito control is the mainstay of dengue prevention and control.
home. The 2022 year has recorded the highest mid-year peak reported         Surveillance and improved reporting of dengue cases is also essential
during the past five years while more than 54% of the reported cases        to prevent and control the disease as indicated in the objectives of the
are from five districts (Colombo, Gampaha, Kaluthara, Kandy and             WHO Global Strategy for Dengue Prevention and Control, 2012–2020.
Galle) of the country with Colombo reporting the highest. At present,       The      mosquitoes      that    spread      dengue          are   active   during     the
almost all districts in the country are reporting cases.                    day. Therefore, personal protective measures should be applied espe-
                                                                            cially during the hours of highest mosquito activity (mid-morning and
Symptoms
                                                                            late afternoon). Lowering the risk of getting dengue by protecting your-
Most people who get dengue won’t have symptoms while symptomatic
                                                                            self from mosquito bites could be done by using protective clothes to
illness may vary from undifferentiated fever, dengue fever (DF), den-
                                                                            cover the body, especially for children in the mornings and afternoons,
gue haemorrhagic fever (DHF) and dengue with unspecified manifes-
                                                                            using physical barriers such as screening doors and windows of prem-
tations. The Onset of sudden high fever, severe headache, pain behind
                                                                            ises using mosquito-proof meshes, using mosquito nets, ideally, nets
the eyes, nausea and pain in muscles and joints are major symptoms
                                                                            sprayed with insect repellent, application of natural repellents such as
of dengue fever while some may also have a rash and varying degrees
                                                                            citronella oil, lemon grass oil, neem oil and chemical repellents con-
of bleeding from various parts of the body including nose, mouth and
                                                                            taining DEET (N, N-Diethyl-m-toluamide). Repellent use must be strict-
skin etc. Most patients get better in 1–2 weeks while some people
                                                                            ly done in accordance with the instructions noticed on the product
develop severe dengue and need care in a hospital. Dengue Haemor-
                                                                            label.
rhagic Fever could be seen only in a small proportion of those infected
                                                                            Dengue transmission is predominantly seen in urban and semi-urban
and is the most severe form with significant bleeding manifestations.
                                                                            areas usually as family or immediate neighbourhood groups of pa-
Patients who are suffering from Severe vomiting, abdominal pain, in-
                                                                            tients. Therefore, if a member of the family or anyone in the immediate
crease thrust, drowsiness and excessive sleepiness, abnormal bleed-
                                                                            neighbourhood is found with dengue, those patients and contacts must
ing manifestations – eg: heavy menstrual bleeding or menstruation
                                                                            be protected from mosquito bites.
starting earlier than usual, and reduced urine output must seek medi-
cal advice even though they don’t have a fever. It is essential to seek     Travellers, especially children, pregnant women, and people with im-
medical attention immediately if the person is suffering from cold clam-    mune disorders or severe chronic illnesses, should contact their doctor
my skin and extremities, restlessness and irritability, skin mottling,      to receive personalized recommendations on the use of repellents and
decreased/no urine output, or behaviour changes like confusion.             protection before travelling. Similar protective measures could be ap-
Diagnosis and treatment                                                     plied to symptomatic patients in order to prevent the disease from
Dengue often goes unrecognized or is misdiagnosed as other fever-           being transmitted to non-infected mosquitoes. Mosquitoes lay eggs in
causing tropical diseases. Early identification and management of           stagnant water which can survive up to one year while eggs can with-
Dengue may minimize morbidity and mortality. When a patient present-        stand dry environmental conditions and thereafter hatch when water is
ed with a high fever with flushed face/extremities and a positive tourni-   available, and the environment is favourable. Therefore, it is very im-
quet test (even with a normal platelet count) with leukopenia (WBC          portant to keep neighbourhoods clean and free of receptacles which
<5000 /mm3) without a focus of infection, mostly suggestive that the        attract                                                                     mosquitoes.
patient is having Dengue illness. Detection of NS1 antigen from blood       Compiled by Dr Nuwandika Siriwardena of the Epidemiology Unit.
is a laboratory diagnostic test for dengue during the early febrile phase
                                                                            Dengue Fact Sheet Situation Report. (2022, July 22). WHO. Retrieved April 26, 2023, from
but NS1 does not help in differentiating Dengue fever from Dengue
                                                                                        https://cdn.who.int/media/docs/default-source/sri-lanka-documents/dengue-fact-
Haemorrhagic Fever.
                                                                                        sheet_7-2022-srl.pdf?sfvrsn=49021bd_1
Dengue patients may also present with atypical manifestations like
                                                                            Murray, N. E. A., Quam, M., & Wilder-Smith, A. (2013, August 20). Epidemiology of dengue:
respiratory symptoms like cough, rhinitis etc. and gastrointestinal
                                                                                        past, present and future prospects. Clinical Epidemiology. Retrieved April 28,
symptoms like constipation, colicky abdominal pain, diarrhoea or vom-
                                                                                        2023, from https://doi.org/10.2147/clep.s34440
iting without classical clinical presentation. Most cases of dengue fever
                                                                            NDCU - Home. (n.d.). National Dengue Control Unit. Retrieved May 1, 2023, from https://



 Page 2.
         RDHS                  Dengue Fever               Dysentery Encephaliti Enteric Fever Food Poi-                      Leptospirosis       Typhus            Viral Hep-       Human             Chickenpox         Meningitis          Leishmania-         WRCD
                               A           B              A      B          A         B        A       B        A   B        A       B           A       B         A        B       A       B         A      B           A       B           A      B            T*      C**
         Colombo                546         7321           0         5          0         9        0       1    0       6    15          149         0       0         0        3       0       0      10        148         1       19       0          5        22      100

         Gampaha                345         7146           0         7          0         10       0       1    0       2        3       269         0       6         0        9       0       0      8         133         0       35       0         19         1       95

         Kalutara               239         2413           0       14           0         1        0       0    0       5    26          384         0       1         0        2       0       1      9         227         0       40       0          1         5      100

         Kandy                  237         2331           0       18           0         0        1       4    0       12       7       124         1       34        0        2       0       1      2         135         0       11       0         14        83      100

         Matale                    44          680         0         2          0         0        0       1    0       5    10          82          2       9         0        3       0       0      0         27          0       3       10         154       19      100

         NuwaraEliya               13          104         7       68           0         1        1       1    0       38       3       50          0       28        0        3       0       0      3         57          0       8        0          0        55      100

         Galle                     92       1091           1       22           1         11       0       5    3       18   19          478         0       26        1        1       0       1      7         173         0       11       0          1        31      100

         Hambantota                41          731         0         4          0         1        0       1    0       8    12          160         0       46        0        7       0       0      4         84          0       14      15         286       26      100
                                                                                                                                                                                                                                                                                                                                                                                                 WER Sri Lanka - Vol. 50 No. 23




         Matara                    65          828         2       17           0         5        0       0    1       7    30          297         1       18        0        2       0       1      8         136         0       9        3         80        48      100

         Jaffna                    44       1472           2       43           0         1        0       8    1       16       0        8          4    457          0        1       0       1      2         109         1       5        0          2        60       93

         Kilinochchi               2           62          0         4          0         0        0       0    0       16       0        7          0       5         0        0       0       0      0          8          0       0        0          0        16       99

         Mannar                    1           62          1         6          0         0        0       1    0       0        0       24          1       5         0        0       0       0      0          1          1       3        0          0        23      100

         Vavuniya                  3           102         0         5          0         1        0       0    0       0        2       25          0       6         0        1       0       0      0         11          0       3        2          5         1      100

         Mullaitivu                11          65          0         8          0         0        0       3    0       11       0       26          0       4         0        0       0       0      0         10          0       0        0          3        20       98

         Batticaloa                79       1574           7      124           0         6        0       3    1       12       9       56          0       1         0        3       1       1      2         36          1       22       0          1        51      100

         Ampara                    0           42          0         1          0         1        0       0    0       0        0       12          0       0         0        1       0       0      0         17          0       7        0          2        16       45

         Trincomalee               82       1620           0         5          0         1        0       0    0       4        6       49          1       13        0        0       0       0      4         28          1       17       0          1        20       98

         Kurunegala                82       1511           4       19           1         7        0       0    1       2    17          177         0       9         0        8       0       2      2         252         3       75       7         217       20       98

         Puttalam                  46       2429           1         7          0         1        0       1    0       0        2       24          0       7         0        1       0       0      2         67          0       28       1         14        13      100

         Anuradhapur               47          354         0         3          0         0        0       1    0       1        3       182         0       23        0        2       0       0      4         128         1       22       5         261       20       98

         Polonnaruwa               22          365         1       10           0         5        0       0    0       6        9       110         0       5         0     10         0       0      1         41          0       13      14         219       31      100

         Badulla                   21          569         0       15           0         3        0       0    0       26       5       149         0       26        3     57         0       0      3         84          1       20       1         13        63      100

         Monaragala                12          295         0       14           0         3        0       0    0       0    12          351         0       27        1     15         0       0      1         39          0       39       2         87        23      100

         Ratnapura                 65       1045           1       20           0         10       0       1    0       9    22          567         0       16        0     12         0       1      5         91          6       96       1         93        33      100

         Kegalle                   99       1442           0       10           0         1        1       2    0       8    30          319         0       18        0        3       0       0      6         211         7       32       0         16        27       99

         Kalmune                   23       1419           1       31           0         7        0       0    0       0        3       26          0       0         0        0       0       0      0         31          0       15       0          0        40       99
         SRILANKA               226 37073 28 482                              2           85   3           34   7   212      24      4105         10      790          5     14       1         9     83      2284        23       547       61      1494         33       98
                                                                                                                                                                                                                                                                                                                                                                                                   03rd– 09th June 2023
                                                                                                                                                                                                                                                                                 Table 1: Selected notifiable diseases reported by Medical Officers of Health 27th– 02nd June 2023 (22nd Week)




Page 3
         Source: Weekly Returns of Communicable Diseases (esurvillance.epid.gov.lk). T=Timeliness refers to returns received on or before 02nd June, 2023 Total number of reporting units 358 Number of reporting units data provided for the current week: 326 C**-Completeness *
         A = Cases reported during the current week. B = Cumulative cases for the year.
WER Sri Lanka - Vol. 50 No.23                                                                                                      03rd– 09th June 2023
Table 2: Vaccine-Preventable Diseases & AFP                                                                             27th– 02nd June 2023(22nd Week)
                                                                                                    Number of     Number of
                                                                                                                               Total                     Difference
                                                                                                    cases         cases                     Total num-
                      No. of Cases by Province                                                      during        during
                                                                                                                               number of
                                                                                                                                            ber of cases
                                                                                                                                                         between the
Disease                                                                                             current       same
                                                                                                                               cases to
                                                                                                                                            to date in
                                                                                                                                                         number of
                                                                                                                               date in                   cases to date
                                                                                                    week in       week in                   2022
                        W        C        S        N        E      NW       NC       U      Sab                                2023                      in 2023 & 2022
                                                                                                    2023          2022

AFP*                    00      00       00       00       00      00      01       00       00         01            01           41            36           13.8 %


Diphtheria              00      00       00       00       00      00      00       00       00         00            00           00            00             0%


Mumps                   00      01       00       00       00      00      00       00       00         01            03           93            27          244.4 %


Measles                 00      02       00       00       00      00      01       00       02         05            00           22            12           83.3 %


Rubella                 00      00       00       00       00      00      00       00       00         00            00           01            00             0%


CRS**                   00      00       00       00       00      00      00       00       00         00            00           00            00             0%


Tetanus                 01      00       00       00       00      00      00       00       01         02            00           05            05             0%

                                                                                                                                                                0%
Neonatal Tetanus        00      00       00       00       00      00      00       00       00         00            00           00            00

Japanese Enceph-
                        00      00       00       00       00      00      00       00       00         00            00           02            07          - 71.4 %
alitis

Whooping Cough          00      00       00       00       00      00      00       00       00         00            00           04            01           300 %


Tuberculosis           124      10       18       25       05      01      16       02       17        218            47         3768          2807           34.2 %


Key to Table 1 & 2
Provinces:          W: Western, C: Central, S: Southern, N: North, E: East, NC: North Central, NW: North Western, U: Uva, Sab: Sabaragamuwa.
RDHS Divisions: CB: Colombo, GM: Gampaha, KL: Kalutara, KD: Kandy, ML: Matale, NE: Nuwara Eliya, GL: Galle, HB: Hambantota, MT: Matara, JF: Jaffna,
                   KN: Killinochchi, MN: Mannar, VA: Vavuniya, MU: Mullaitivu, BT: Batticaloa, AM: Ampara, TR: Trincomalee, KM: Kalmunai, KR: Kurunegala, PU: Puttalam,
                   AP: Anuradhapura, PO: Polonnaruwa, BD: Badulla, MO: Moneragala, RP: Ratnapura, KG: Kegalle.
Data Sources:
Weekly Return of Communicable Diseases: Diphtheria, Measles, Tetanus, Neonatal Tetanus, Whooping Cough, Chickenpox, Meningitis, Mumps., Rubella, CRS,
Special Surveillance: AFP* (Acute Flaccid Paralysis ), Japanese Encephalitis
CRS** =Congenital Rubella Syndrome
NA = Not Available



   Take prophylaxis medications for leptospirosis during the paddy cultiva-
                       tion and harvesting seasons.
               It is provided free by the MOH office / Public Health Inspectors.


Comments and contributions for publication in the WER Sri Lanka are welcome. However, the editor reserves the right to accept or reject
items for publication. All correspondence should be mailed to The Editor, WER Sri Lanka, Epidemiological Unit, P.O. Box 1567, Colombo or
sent by E-mail to chepid@sltnet.lk. Prior approval should be obtained from the Epidemiology Unit before pub-
lishing data in this publication

                                                             ON STATE SERVICE
Dr. Samitha Ginige
Actg. CHIEF EPIDEMIOLOGIST
EPIDEMIOLOGY UNIT
231, DE SARAM PLACE
COLOMBO 10
"""

#test string 3
TEST_STRING3 = """     WEEKLY EPIDEMIOLOGICAL REPORT
                    A publication of the Epidemiology Unit
                               Ministry of Health
                   231, de Saram Place, Colombo 01000, Sri Lanka
       Tele: + 94 11 2695112, Fax: +94 11 2696583, E mail: epidunit@sltnet.lk
              Epidemiologist: +94 11 2681548, E mail: chepid@sltnet.lk
                            Web: http://www.epid.gov.lk

 Vol. 40 No.21                                                                             18th – 24th May 2013
                         Vector-Borne Viral Infections
 Numerous diseases are transmitted by insect                  Some of these viruses belong to Flaviviridae
 vectors. Most are restricted to the tropical coun-           family. They are,
 tries and are only seen in more temperate re-                • Yellow fever virus (YFV)
 gions as imported diseases due to the require-
 ments of the vectors concerned.                              • Dengue fever viruses (DV)
                                                              • Japanese encephalitis virus (JEV)
 In addition to Protozoal infections [e.g. Afri-
 can trypanosomiasis (sleeping sickness), Try-
                                                              • West Nile virus (WNV)
 panosoma brucei, American trypanosomiasis                    • Tick-borne encephalitis virus (TBEV)
 (Chagas disease), Trypanosoma cruzi,                         • Murray Valley encephalitis
 Leishmaniasis, Malaria], a great many viruses
 also are transmitted by arthropod bites. Most of             • Omsk haemorrhagic fever
 these infections are caused by mosquitoes or                 • Kyasanur Forest disease and the
 ticks and for that reason fall under the generic
 name of "arboviruses" (arthropod-borne vi-
                                                              • Saint-Louis encephalitis (SLE) viruses
 ruses) Most of these viruses belong to the Al-
                                                              Several members of the Bunyamviridae family
 phaviridae family.
                                                              also are transmitted by mosquitoes, such as
 They are,
                                                              • Rift Valley fever virus (RVFV)
 • Eastern, Western and Venezuelan equine                     • California encephalitis virus
   encephalitis viruses (EEEV, WEEV and                       • Crimean-Congo hemorrhagic fever (CCHF)
   VEEV, respectively),                                             virus are transmitted by ticks. Several of
 • O'nyong nyong                                                    these viruses are the agents of viral haemor-
 • Chikungunya virus                                                rhagic fever (Please referTable1).


Table 1– Viral Haemorrhagic Fevers (Source– WHO)
        Disease               Annual Incidence                          Vector               Animal Reservoir
    Congo-Crimean HF                                                                          Hares, Crows, Cows, Os-
                                        1000’s                       Ticks (Hyalomma)
        (CCHF)                                                                                         triches
                                                             Mosquitoes (Ae aegypti, Ae
     Dengue/DHF/DSS                250 000-500 000                                                     None
                                                                    albopictus)
     Kyasanur Forest
                                         100’s                     Ticks (Haemaphysalis)      Monkeys, Rodents, Birds
      Disease (KFD)

    Omsk Haemorrhagic
                                         100’s                      Ticks (Dermacentor)            Field Mouse
          Fever

                                                             Mosqitoes (Culex pipiens, Ae
     Rift Valley Fever                 10 000’s                                                Sheep, Cattle, Camels
                                                              africanus, Anopheles, etc)
                             200 000 before vaccine intro-    Mosqitoes (Ae aegypti and
     Yellow Fever (YF)                                                                               Monkeys
                                       duction                 others, Haemagogus)

                                                  Contents                                                     Page
1. Leading Article – Vector-Borne Viral Infections                                                               1
2. Surveillance of vaccine preventable diseases & AFP (11th – 17th May 2013)                                     3
3. Summary of newly introduced notifiable diseases (11 – 17 May 2013)
                                                       th     th                                                 3
4. Summary of selected notifiable diseases reported (11th – 17th May 2013)                                       4
WER Sri Lanka - Vol. 40 No. 21                                                                               18th – 24th May 2013
Not surprisingly, arboviruses can cause vast epidemics with          for Lyme disease and for louse-borne and tick-borne relaps-
impressive numbers of cases of illness or deaths. Dengue,            ing fevers, Yersinia pestis, the agent of plague or Bartonellas
the most prevalent mosquito-borne viral disease, is estimated        and Rickettsias that are responsible for a variety of spotted
to cause 100 million infections each year, 250 000-500 000 of        fevers, including the Rocky Mountain spotted fever, typhus
which are the cause of severe illness. Major epidemics of JE         and Q fever.
were reported from India and Nepal during the past few
years. Rift Valley fever is endemic in Western and Eastern-          Dengue, Japanese encephalitis (JE) and Malaria are the
Africa where epidemic outbreaks in thousands of humans               three most important mosquito-borne diseases in terms of
parallel epizootic outbreaks in sheep and cattle. More than          morbidity and mortality. A vaccine is already available for
265 000 people were infected during the recent Chikungunya           Japanese Encephalitis (JE) and hopefully, vaccines will be
outbreak in Réunion, as well as 1 400 000 people in 2006 in          available for the other two within the next five years; and with
India. Japanese encephalitis accounts for up to 50 000 cases         leishmaniasis, for which there unfortunately is no hope of a
of encephalitis every year with case fatality rates of about         vaccine soon.
25%.
                                                                     Source-Vector-Borne Viral Infections, available from http://
Other viruses that cause haemorrhagic fevers, such as the
                                                                     www.who.int/vaccine_research/diseases/vector/en/
Hantavirus (Haemorrhagic fever with renal syndrome),
Arenaviruses (Lassa virus, Junin virus) or filoviruses (Ebola,       Compiled by Dr. Madhava Gunasekera of the Epidemiology Unit
Marburg) are not vector-borne.
Significant epidemics of yellow fever have been found to oc-         Table 3 : Water Quality Surveillance
cur almost every year in western Africa, with an estimated
                                                                     Number of microbiological water samples - April / 2013
record 44 000 cases and 25 000 deaths in Nigeria in 1987-
88. A 2001 YF outbreak in Abidjan, Côte d'Ivoire, required           District          MOH areas       No: Expected *   No: Received
immunizing 2.6 million persons in 12 days. WHO estimates
that there may be up to 200 000 cases of YF a year in west-          Colombo                 12                72            69
ern Africa, with 30 000 deaths, prompted GAVI and WHO to             Gampaha                 15                90            34
launch a major initiative to vaccinate more than 48 million
people in 12 West African countries over the next 5 years,           Kalutara                12                72            26
using the live attenuated 17D YF vaccine, which is mandatory         Kalutara NI             2                 12            14
for travellers to endemic areas of Africa and South America.
                                                                     Kandy                   23               138            15
The epidemiology of arbovirus infection in man is influenced
by the probability of contacts between the vector, the human         Matale                  12                72            16
population and for many viruses, the amplifying vertebrate           Nuwara Eliya            13                78            18
host, whether birds (most arboviruses that cause encephali-
tis), monkeys (YFV, KFV), horses (EEEV, WEEV, VEEV,                  Galle                   19               114            NR
WNV), sheep (RVF), pigs (JEV) or rodents, which serve as             Matara                  17               102            17
reservoir for the virus. Several arboviral infections are actually
expanding geographically, as exemplified by the emergence            Hambantota              12                72            26
of WNV in the Americas or JEV in Australasia, the spread of
                                                                     Jaffna                  11                66            33
dengue, the re-emergence of YFV in South America and the
recent outbreak of Chikungunya in northern Italy. Both yellow        Kilinochchi             4                 24            19
fever and dengue are transmitted between humans by Aedes
                                                                     Manner                  5                 30            20
aegypti, which are anthropophilic mosquitoes that breed in
urban dwellings. Why is dengue virus much more widespread            Vavuniya                4                 24            38
than yellow fever virus, which has never appeared in Asia, is
not known. It may have to do with the fact that dengue occurs        Mullatvu                4                 24             0
mainly in urban areas whereas outbreaks of yellow fever              Batticaloa              14                84            26
arise in remote areas. Moreover, dengue virus can be trans-
mitted transovarially and sexually through mosquito popula-          Ampara                  7                 42             0
tions.                                                               Trincomalee             11                66            NR
Japanese encephalitis is widespread over South and South             Kurunegala              23               138            110
East Asia and Australasia, from Pakistan to the shores of
Australia. The virus infects Culex spp mosquitoes that feed          Puttalam                9                 84            88
on birds, humans, pigs, horses and breed in rice paddy fields.
                                                                     Anuradhapura            19               114            32
New irrigation projects that support agricultural development
therefore increase the risk of disease outbreaks. As to West         Polonnaruwa             7                 42             6
Nile virus, it attracted attention as a major pathogen after an
                                                                     Badulla                 15                90            NR
unexpected outbreak of fever and encephalitis occurred in
New York City in August 1999. Within a few weeks of its              Moneragala              11                66            74
emergence on the American continent there were 62 con-
firmed cases and seven deaths among elderly people. The              Rathnapura              18               108             8
virus, which most likely had been introduced from Israel or          Kegalle                 11                66            66
Egypt dispersed and spread throughout North America within
the next five years.                                                 Kalmunai                13                78             0

In addition to protozoans and viruses, arthropods can also           * No of samples expected (6 / MOH area / Month)
transmit bacteria, such as Borrelia spirochaetes responsible         NR = Return not received

Page 2
WER Sri Lanka - Vol. 40 No. 21                                                                                                        18th – 24th May 2013
Table 1: Vaccine-preventable Diseases & AFP                                                                                11th – 17thMay 2013 (20th Week)
Disease                                         No. of Cases by Province                           Number of Number of    Total            Total num-      Difference
                                                                                                     cases     cases   number of             ber of       between the
                                                                                                    during    during    cases to            cases to       number of
                                                                                                    current    same      date in             date in      cases to date
                                                                                                    week in   week in     2013                2012       in 2013 & 2012
                       W        C          S        N          E    NW      NC     U         Sab
                                                                                                     2013      2012




Acute Flaccid          00       01      01         00          00    00     00     00        00        02           01           29            33          - 12.1 %
Paralysis
                       00       00      00         00          00    00     00     00        00         -            -            -             -               -
Diphtheria

                       24       16      10         00          00    01     01     00        01        53           00           402           20        + 1910.0 %
Measles

                       00       00      00         00          00    00     00     00        00        00           00           07            04          + 75.0 %
Tetanus

Whooping               02       00      00         00          00    00     00     00        01        03           00           34            32          - 06.3 %
Cough
                       33       54      56         32          28    27     00     14        43       257          206           3137         3402         - 07.8 %
Tuberculosis

Table 2: Newly Introduced Notifiable Disease                                                                               11th – 17thMay 2013 (20th Week)
    Disease                                     No. of Cases by Province                           Number of Number of    Total            Total num-      Difference
                                                                                                     cases     cases   number of             ber of       between the
                        W         C        S        N          E    NW      NC      U        Sab    during    during    cases to            cases to       number of
                                                                                                    current    same      date in             date in      cases to date
                                                                                                    week in   week in     2013                2012       in 2013 & 2012
                                                                                                     2013       2012

Chickenpox              11       08        09      09        02     05      02     03        05        54            04          1842        1953           - 5.7 %

                        04       00        03      02        00     03      02     00        00        14            00          467          235         + 98.7 %
                       KL=1             MT=2      VU=1              KR=3   AP=2
Meningitis             GM=2             GL=1      JF=1
                       CL=1



Mumps                   01       00        04      04        00     03      01     03        05        21            05          657         1889          - 65.2 %

                        01       00        08      00        01     00      05     03        00        18            00          433          236         + 83.5 %
Leishmaniasis          KL=1             MT=2                TR=1           AP=5   BD=3
                                        HB=6

Influenza Surveillance in Sentinel Hospitals - ILI & SARI
                 Human                                                                                            Animal
Month
                No Received      Infl A untyped          Infl B     A(H1N1)pdm09       A(H3N2)         RSV        Pooled samples        Serum Samples        Positives
April                360               7                  21               26            8              2                  306                  240                 0
Source: Medical Research Institute & Veterinary Research Institute
Key to Table 1 & 2
Provinces:          W: Western, C: Central, S: Southern, N: North, E: East, NC: North Central, NW: North Western, U: Uva, Sab: Sabaragamuwa.
DPDHS Divisions: CB: Colombo, GM: Gampaha, KL: Kalutara, KD: Kandy, ML: Matale, NE: Nuwara Eliya, GL: Galle, HB: Hambantota, MT: Matara, JF: Jaffna,
                    KN: Killinochchi, MN: Mannar, VA: Vavuniya, MU: Mullaitivu, BT: Batticaloa, AM: Ampara, TR: Trincomalee, KM: Kalmunai, KR: Kurunegala, PU: Puttalam,
                    AP: Anuradhapura, PO: Polonnaruwa, BD: Badulla, MO: Moneragala, RP: Ratnapura, KG: Kegalle.
Data Sources:
Weekly Return of Communicable Diseases: Diphtheria, Measles, Tetanus, Whooping Cough, Chickenpox, Meningitis, Mumps.
Special Surveillance: Acute Flaccid Paralysis.


                                       Dengue Prevention and Control Health Messages
        Check the roof gutters regularly for water collection
              where dengue mosquitoes could breed.

                                                                                                                                                           Page 3
WER Sri Lanka - Vol. 40 No. 21                                                                                                                18th – 24th May 2013
Table 4: Selected notifiable diseases reported by Medical Officers of Health
                                                                                                                                     11th– 17thMay 2013 (20th Week)
   DPDHS           Dengue Fe-         Dysentery        Encephali        Enteric         Food    Leptospirosi              Typhus            Viral          Human         Returns
   Division        ver / DHF*                             tis            Fever        Poisoning      s                     Fever          Hepatitis        Rabies          Re-
                                                                                                                                                                         ceived

                   A         B         A        B       A      B       A       B       A       B       A        B        A       B        A       B       A       B        %
Colombo            55      3334        5       67       0      10      1      49       0       14       2      115       0       5        2      34       0       0        54
Gampaha            35      1440        1       52       0       7      0      15       1       13       6      141       0       8        1      93       0       0        47

Kalutara           37       686        4       58       1      11      0      35       0       9       10      190       0       1        0       7       0       0        77

Kandy              28       709        6       48       0       6      0       9       0       7        2       35       5       60       1      52       0       0        74

Matale             1        194        0       35       0       1      1       6       0       0        1       25       0       2        0      20       0       0        77

NuwaraEliya        5        103        5       75       0       2      0       4       0       2        1       12       0       35       0      11       0       0        62

Galle              11       308        0       35       0       8      0       2       0       4        0      108       0       22       0       6       0       1        53

Hambantota         5        147        0       22       0       2      0       7       0       9        2      119       1       36       1      63       0       0        67

Matara             9        236        2       26       0       8      1      10       0       27       5      100       0       35       2      98       1       2       100

Jaffna             9        420        2       85       0       4      8      216      0       7        1       5        0      308       0       9       0       0        75

Kilinochchi        0        25         0       12       0       0      0       5       1       2        0       9        0       14       0       0       0       0        25

Mannar             4        51         0       21       0       1      1      48       0       11       0       9        1       15       0       0       0       0        80

Vavuniya           0        38         0       22       0      10      0       5       0       8        0       36       0       2        0       0       0       1       100
Mullaitivu         2        65         0        6       0       1      0       6       0       3        4       15       0       5        0       0       0       2        80

Batticaloa         2        314        2       80       0       3      0       0       2       7        1       22       0       2        0       8       0       0        43

Ampara             0        59         0       40       0       0      0       4       0       0        0       7        0       0        0       1       0       0        14

Trincomalee        4        134        3       32       0       1      0       2       0       1        0       46       0       4        0       3       0       1        67

Kurunegala         18      1727        0       82       1      23      0      23       0       3        4      152       1       16       0      28       0       1        73

Puttalam           9        534        1       25       0       4      1       9       0       34       1       13       0       9        0       1       0       0        46

Anuradhapu         5        304        0       32       0      12      0       2       0       2        3      231       0       15       0      12       0       0        47

Polonnaruw         1        177        0       37       0       0      0       9       0       0        0      100       0       2        0      18       0       1        57

Badulla            3        196        2       58       0       1      0       7       0       1        0       16       0       29       1      23       0       0        71

Monaragala         4        113        5       43       0       3      1       8       0       18       6      165       1       24       2      38       0       1        73

Ratnapura          16       837        3      177       0      77      0      21       0       12       1      190       0       15       2      118      0       1        50
Kegalle            19       489        1       26       0      10      1       7       0       3        0       60       3       46       3      110      0       0        91

Kalmune            2        431        3       52       0       1      0       3       2       23       0       4        0       2        0       4       0       0        38
 SRI LANKA       284     13071        45     1248      02     206     15     512      06     220       50     1925      12     712       15     757      01      11        63

Source: Weekly Returns of Communicable Diseases WRCD).
*Dengue Fever / DHF refers to Dengue Fever / Dengue Haemorrhagic Fever.
**Timely refers to returns received on or before 17th May, 2013 Total number of reporting units 336. Number of reporting units data provided for the current week: 246
A = Cases reported during the current week. B = Cumulative cases for the year.

                 PRINTING OF THIS PUBLICATION IS FUNDED BY THE WORLD HEALTH ORGANIZATION (WHO).
Comments and contributions for publication in the WER Sri Lanka are welcome. However, the editor reserves the right to accept or reject
items for publication. All correspondence should be mailed to The Editor, WER Sri Lanka, Epidemiological Unit, P.O. Box 1567, Colombo or
sent by E-mail to chepid@sltnet.lk.
                                                                    ON STATE SERVICE


Dr. P. PALIHAWADANA
CHIEF EPIDEMIOLOGIST
EPIDEMIOLOGY UNIT
231, DE SARAM PLACE
COLOMBO 10
"""

if __name__ == "__main__":
    extract_data_from_rtf(TEST_STRING2)
