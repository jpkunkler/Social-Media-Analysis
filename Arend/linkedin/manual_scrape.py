import csv

with open('linkedin_analysis.csv', 'w') as file:
    w = csv.writer(file)
    w.writerow(['company', 'employees', 'employees_on_linkedin', 'follower',
                'updates', 'open_jobs'])

    cont = True
    while cont:
        company = raw_input("Company Name: ")
        employees = raw_input('Employees: ')
        employees_on_linkedin = raw_input('Employees on LinkedIn: ')
        follower = raw_input('Followers: ')
        updates = raw_input('Updates: ')
        jobs = raw_input('Jobs: ')
        print "-"*10
        print "Company: ", company
        print "Employees: ", employees
        print "Employees on LinkedIn: ", employees_on_linkedin
        print "Follower: ", follower
        print "Updates: ", updates
        print "Jobs: ", jobs
        choice = raw_input("Are these values correct?(y/n): ")
        if 'y' in choice.lower():
            w.writerow([company, employees, employees_on_linkedin, follower, updates, jobs])
        choice = raw_input('Do you want to scrape another company?(y/n): ')
        if 'n' in choice.lower():
            cont = False
