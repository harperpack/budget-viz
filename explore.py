import pandas as pd
import numpy as np
import json

budget_data = "/Users/harper/Documents/harper_files/projects/budget_data/2019__2020__and_2021_Budget_Data.csv"

bdf = pd.read_csv(budget_data)

# accounts = ['Revenues','Expenses']

# budget = {}
# print(bdf.head())
# print(1/0)

class SubAccount:

    def __init__(self, name):
        self.name = name
        self.revenue = 0
        self.expense = 0

class Account:

    def __init__(self, name):
        self.name = name
        self.sub_accounts = []
        self.revenue = 0
        self.expense = 0

    def fetch_subs(self, sub):
        match = [sub_account for sub_account in self.sub_accounts if sub_account.name == sub]
        if not match:
            self.sub_accounts.append(SubAccount(sub))
            return self.sub_accounts[-1]
        elif len(match) > 1:
            print("ERROR: Duplicate accts with {a}".format(a=sub))
        else:
            return match[0]

class Fund:

    def __init__(self, name):
        self.name = name
        self.revenue = 0
        self.expense = 0

class Unit:

    def __init__(self, name):
        self.name = name
        self.revenue = 0
        self.expense = 0
        self.accounts = []
        self.sub_accounts = []

    def fetch_account(self, acct):
        match = [account for account in self.accounts if account.name == acct]
        if not match:
            self.accounts.append(Account(acct))
            return self.accounts[-1]
        elif len(match) > 1:
            print("ERROR: Duplicate accts with {a}".format(a=acct))
        else:
            return match[0]

    def fetch_subs(self, sub):
        match = [sub_account for sub_account in self.sub_accounts if sub_account.name == sub]
        if not match:
            self.sub_accounts.append(SubAccount(sub))
            return self.sub_accounts[-1]
        elif len(match) > 1:
            print("ERROR: Duplicate subs with {a}".format(a=sub))
        else:
            return match[0]

class Dept:

    def __init__(self, name):
        self.name = name
        self.funds = []
        self.units = []
        self.accounts = []
        self.sub_accounts = []
        self.revenue = 0
        self.expense = 0

    def fetch_fund(self, fund):
        match = [fnd for fnd in self.funds if fnd.name == fund]
        if not match:
            self.funds.append(Fund(fund))
            return self.funds[-1]
        elif len(match) > 1:
            print("ERROR: Duplicate funds with {a}".format(a=fund))
        else:
            return match[0]

    def fetch_unit(self, unit):
        if unit.upper() in ['CITY CLERK','CITY COUNCIL','REPARATIONS FUND','HOME FUND','INTERFUND TRANSFERS','SPECIAL ASSESSMENT']:
            unit = unit.replace(' ','_')
        match = [b_unit for b_unit in self.units if b_unit.name == unit]
        if not match:
            self.units.append(Unit(unit))
            return self.units[-1]
        elif len(match) > 1:
            print("ERROR: Duplicate funds with {a}".format(a=unit))
        else:
            return match[0]

    def fetch_account(self, acct):
        match = [account for account in self.accounts if account.name == acct]
        if not match:
            self.accounts.append(Account(acct))
            return self.accounts[-1]
        elif len(match) > 1:
            print("ERROR: Duplicate accts with {a}".format(a=acct))
        else:
            return match[0]

    def fetch_subs(self, sub):
        match = [sub_account for sub_account in self.sub_accounts if sub_account.name == sub]
        if not match:
            self.sub_accounts.append(SubAccount(sub))
            return self.sub_accounts[-1]
        elif len(match) > 1:
            print("ERROR: Duplicate subs with {a}".format(a=sub))
        else:
            return match[0]

class Budget:

    def __init__(self, name, df, output):
        self.name = name
        self.funds = []
        self.depts = []
        self.units = []
        self.accounts = []
        self.sub_accounts = []
        self.revenue = 0
        self.expense = 0
        self.type_name = "Account Type"
        self.fund_name = "Fund"
        self.dept_name = "Department"
        self.unit_name = "Business Unit"
        self.acct_name = "Account Classification"
        self.subs_name = "Account Code And Description"
        self.vals_name = ["2019 Adopted Budget","2020 Adopted Budget","2021 Projected Budget"]
        self.main(df, output)

    def obtain_value(self, row):
        sum = 0
        for val_name in self.vals_name:
            sum += float(row[val_name].replace(",",''))
        #print(sum / len(self.vals_name))
        return int(sum / len(self.vals_name))

    def get_objects(self, row):
        # top level
        dept = self.fetch_dept(row[self.dept_name].title())
        fund = self.fetch_fund(row[self.fund_name].title())
        unit = self.fetch_unit(row[self.unit_name].title())
        account = self.fetch_account(row[self.acct_name].title())
        sub_account = self.fetch_subs(row[self.subs_name].title())
        # dept level
        dept_fund = dept.fetch_fund(row[self.fund_name].title())
        dept_unit = dept.fetch_unit(row[self.unit_name].title())
        dept_account = dept.fetch_account(row[self.acct_name].title())
        dept_sub_account = dept.fetch_subs(row[self.subs_name].title())
        # unit level
        unit_account = dept_unit.fetch_account(row[self.acct_name].title())
        unit_sub_account = dept_unit.fetch_subs(row[self.subs_name].title())
        # account level
        account_sub_account = unit_account.fetch_subs(row[self.subs_name].title())
        return [dept, fund, unit, account, sub_account, dept_fund, dept_unit, dept_account, dept_sub_account, unit_account, unit_sub_account, account_sub_account]

    def tally_row(self, row):
        value = self.obtain_value(row)
        objects = self.get_objects(row)
        if row[self.type_name] == "Revenues":
            for obj in objects:
                obj.revenue += value
            self.revenue += value
        elif row[self.type_name] == "Expenses":
            for obj in objects:
                obj.expense += value
            self.expense += value
        else:
            print("ERROR: Unknown classification with {t}".format(t=row["Account Type"]))

    def fetch_dept(self, dept):
        match = [department for department in self.depts if department.name == dept]
        if not match:
            self.depts.append(Dept(dept))
            return self.depts[-1]
        elif len(match) > 1:
            print("ERROR: Duplicate depts with {d}".format(d=dept))
        else:
            return match[0]

    def fetch_fund(self, fund):
        match = [fnd for fnd in self.funds if fnd.name == fund]
        if not match:
            self.funds.append(Fund(fund))
            return self.funds[-1]
        elif len(match) > 1:
            print("ERROR: Duplicate funds with {d}".format(d=fund))
        else:
            return match[0]

    def fetch_unit(self, unit):
        if unit.upper() in ['CITY CLERK','CITY COUNCIL','REPARATIONS FUND','HOME FUND','INTERFUND TRANSFERS','SPECIAL ASSESSMENT']:
            unit = unit.replace(' ','_')
        match = [b_unit for b_unit in self.units if b_unit.name == unit]
        if not match:
            self.units.append(Unit(unit))
            return self.units[-1]
        elif len(match) > 1:
            print("ERROR: Duplicate units with {d}".format(d=unit))
        else:
            return match[0]

    def fetch_account(self, acct):
        match = [account for account in self.accounts if account.name == acct]
        if not match:
            self.accounts.append(Account(acct))
            return self.accounts[-1]
        elif len(match) > 1:
            print("ERROR: Duplicate accts with {a}".format(a=acct))
        else:
            return match[0]

    def fetch_subs(self, sub):
        match = [sub_account for sub_account in self.sub_accounts if sub_account.name == sub]
        if not match:
            self.sub_accounts.append(SubAccount(sub))
            return self.sub_accounts[-1]
        elif len(match) > 1:
            print("ERROR: Duplicate accts with {a}".format(a=sub))
        else:
            return match[0]

    def format(self, number):
        num = str(int(number))
        length = len(num)
        if length < 4:
            return ''.join(['$',num])
        output = ''
        while length > 3:
            output = num[-3:] + output
            output = ',' + output
            num = num[:-3]
            length = len(num)
        output = '$' + num + output
        return output

    def ratio(self, numerator, denominator):
        if denominator:
            return int(100 * (numerator/denominator))
        elif numerator:
            return "ERROR"
        else:
            return 'n/a'

    def classify(self, name):
        if name in [x.name for x in self.depts]:
            return "department"
        elif name in [x.name for x in self.funds]:
            return "fund"
        elif name in [x.name for x in self.units]:
            return "unit"
        elif name in [x.name for x in self.accounts]:
            return "account"
        elif name in [x.name for x in self.sub_accounts]:
            return "sub_account"
        else:
            print("ERROR: cannot locate {n}".format(n=name))

    def output(self):
        budget = {"revenue":{},"expense":{}}
        budget["revenue"][self.name] = {"type":"total","members":{"total":(self.revenue, self.ratio(self.revenue,self.revenue))}}
        budget["expense"][self.name] = {"type":"total","members":{"total":(self.expense, self.ratio(self.expense,self.expense))}}
        #print([x.name for x in self.depts if x.name in [y.name for y in self.funds]])
        # print([x.name for x in self.depts if x.name in [y.name for y in self.units]])
        # print([x.name for x in self.funds if x.name in [y.name for y in self.units]])
        #print([x.name for x in self.depts if x.name in [y.name for y in self.accounts]])
        #print([x.name for x in self.depts if x.name in [y.name for y in self.sub_accounts]])
        # print(sorted([x.name for x in self.depts]))
        # print(sorted([x.name for x in self.funds]))
        #print(sorted([x.name for x in self.units]))
        # print(sorted([x.name for x in self.accounts]))
        # print(sorted([x.name for x in self.sub_accounts]))
        # print(1/0)
        all_objs = self.depts + self.funds + self.units + self.accounts + self.sub_accounts
        for obj in all_objs:
            obj_type = self.classify(obj.name)
            if obj.revenue:
                if not budget["revenue"].get(obj.name,''):
                    budget["revenue"][obj.name] = {"type":obj_type,"members":{"total":(obj.revenue,self.ratio(obj.revenue,self.revenue))}}
                else:
                    print("ERROR: duplicate rev dept with {o}".format(o=obj.name))
            if obj.expense:
                if not budget["expense"].get(obj.name,''):
                    budget["expense"][obj.name] = {"type":obj_type,"members":{"total":(obj.expense,self.ratio(obj.expense,self.expense))}}
                else:
                    print("ERROR: duplicate exp dept with {o}".format(o=obj.name))
        for dept in self.depts:
            all_objs = dept.funds + dept.units + dept.accounts + dept.sub_accounts
            for obj in all_objs:
                if obj.revenue:
                    if not budget["revenue"].get(obj.name,''):
                        obj_type = self.classify(obj.name)
                        budget["revenue"][obj.name] = {"type":obj_type,"members":{dept.name:(obj.revenue,self.ratio(obj.revenue,dept.revenue))}}
                    else:
                        budget["revenue"][obj.name]["members"][dept.name] = (obj.revenue,self.ratio(obj.revenue,dept.revenue))
                if obj.expense:
                    if not budget["expense"].get(obj.name,''):
                        obj_type = self.classify(obj.name)
                        budget["expense"][obj.name] = {"type":obj_type,"members":{dept.name:(obj.expense,self.ratio(obj.expense,dept.expense))}}
                    else:
                        budget["expense"][obj.name]["members"][dept.name] = (obj.expense,self.ratio(obj.expense,dept.expense))
            for unit in dept.units:
                all_objs = unit.accounts + unit.sub_accounts
                for obj in all_objs:
                    if obj.revenue:
                        if not budget["revenue"].get(obj.name,''):
                            obj_type = self.classify(obj.name)
                            budget["revenue"][obj.name] = {"type":obj_type,"members":{unit.name:(obj.revenue,self.ratio(obj.revenue,unit.revenue))}}
                        else:
                            budget["revenue"][obj.name]["members"][unit.name] = (obj.revenue,self.ratio(obj.revenue,unit.revenue))
                    if obj.expense:
                        if not budget["expense"].get(obj.name,''):
                            obj_type = self.classify(obj.name)
                            budget["expense"][obj.name] = {"type":obj_type,"members":{unit.name:(obj.expense,self.ratio(obj.expense,unit.expense))}}
                        else:
                            budget["expense"][obj.name]["members"][unit.name] = (obj.expense,self.ratio(obj.expense,unit.expense))
                for account in unit.accounts:
                    for obj in account.sub_accounts:
                        if obj.revenue:
                            if not budget["revenue"].get(obj.name,''):
                                obj_type = self.classify(obj.name)
                                budget["revenue"][obj.name] = {"type":obj_type,"members":{account.name:(obj.revenue,self.ratio(obj.revenue,account.revenue))}}
                            else:
                                budget["revenue"][obj.name]["members"][account.name] = (obj.revenue,self.ratio(obj.revenue,account.revenue))
                        if obj.expense:
                            if not budget["expense"].get(obj.name,''):
                                obj_type = self.classify(obj.name)
                                budget["expense"][obj.name] = {"type":obj_type,"members":{account.name:(obj.expense,self.ratio(obj.expense,account.expense))}}
                            else:
                                budget["expense"][obj.name]["members"][account.name] = (obj.expense,self.ratio(obj.expense,account.expense))
        with open("./budget.json", 'w', encoding='utf-8') as f:
            json.dump(budget, f, ensure_ascii=False, indent=4)



    def rank_print(self):
        ranked_rev_depts = reversed(sorted(self.depts, key=lambda dept: dept.revenue))
        ranked_exp_depts = reversed(sorted(self.depts, key=lambda dept: dept.expense))
        ranked_rev_accts = reversed(sorted(self.accounts, key=lambda acct: acct.revenue))
        ranked_exp_accts = reversed(sorted(self.accounts, key=lambda acct: acct.expense))
        print("Departments by Revenue: \n")
        for rank, dept in enumerate(ranked_rev_depts, start=1):
            ratio = self.ratio(dept.revenue,self.revenue)
            if ratio < 5:
                leftover = len(self.depts) - rank
                print("{r} - {f}:  Other ({l} departments)".format(r=rank,f=rank+leftover,l=leftover))
                break
            print("{r}:  {d}\n\t{m}\t({x}%)\n".format(r=rank,d=dept.name,m=self.format(dept.revenue),x=ratio))
        print("-----\nDepartments by Expense: \n")
        for rank, dept in enumerate(ranked_exp_depts, start=1):
            ratio = self.ratio(dept.expense,self.expense)
            if ratio < 5:
                leftover = len(self.depts) - rank
                print("{r} - {f}:  Other ({l} departments)".format(r=rank,f=rank+leftover,l=leftover))
                break
            print("{r}:  {d}\n\t{m}\t({x}%)\n".format(r=rank,d=dept.name,m=self.format(dept.expense),x=ratio))
        print("\n=====\nAccounts by Revenue: \n")
        for rank, acct in enumerate(ranked_rev_accts, start=1):
            ratio = self.ratio(acct.revenue,self.revenue)
            if ratio < 5:
                leftover = len(self.accounts) - rank
                print("{r} - {f}:  Other ({l} accounts)".format(r=rank,f=rank+leftover,l=leftover))
                break
            print("{r}:  {d}\n\t{m}\t({x}%)\n".format(r=rank,d=acct.name,m=self.format(acct.revenue),x=ratio))
        print("-----\nAccounts by Expense: \n")
        for rank, acct in enumerate(ranked_exp_accts, start=1):
            ratio = self.ratio(acct.expense,self.expense)
            if ratio < 5:
                leftover = len(self.accounts) - rank
                print("{r} - {f}:  Other ({l} accounts)".format(r=rank,f=rank+leftover,l=leftover))
                break
            print("{r}:  {d}\n\t{m}\t({x}%)\n".format(r=rank,d=acct.name,m=self.format(acct.expense),x=ratio))

    def verbose_print(self):
        print("Total budget for {n}:".format(n=self.name))
        print(">Revenue: {r}".format(r=self.format(self.revenue)))
        print(">Expense: {e}".format(e=self.format(self.expense)))
        print("------\n")
        for dept in self.depts:
            print("{d}:".format(d=dept.name))
            print("->Total Revenue: {r}\t({x}% of total)".format(r=self.format(dept.revenue),x=self.ratio(dept.revenue,self.revenue)))
            print("->Total Expense: {e}\t({x}% of total)".format(e=self.format(dept.expense),x=self.ratio(dept.expense,self.expense)))
            print("\n")
            for acct in dept.accounts:
                print('--{a}'.format(a=acct.name))
                print('---> R: {r}\t({x}%)'.format(r=self.format(acct.revenue),x=self.ratio(acct.revenue,dept.revenue)))
                print('---> E: {e}\t({x}%)'.format(e=self.format(acct.expense),x=self.ratio(acct.expense,dept.expense)))

    def main(self, df, output):
        for index, row in df.iterrows():
            self.tally_row(row)
        # print(count)
        # print(len(self.revenue) + len(self.expense))
        # print(self.revenue)
        # print(self.expense)
        # print(1/0)
        if output == "verbose":
            self.verbose_print()
        elif output == "rank":
            self.rank_print()
        elif output == "output":
            self.output()

Budget("Evanston",bdf,"output")


# cols = []
# for col in bdf:
#     if col == "Account Type":
#         continue
#     elif col in ["2019 Adopted Budget","2020 Adopted Budget","2021 Projected Budget"]:
#         continue
#     cols.append(col)
#
# for index, row in bdf.iterrows():
#     dept = row["Department"]
#     unit = row["Business Unit"]
#     amount = float(row["2020 Adopted Budget"].replace('.','').replace(',',''))
#     type = row["Account Type"]
#     if not budget.get(dept,''):
#         #budget[dept] = {"R19":0,"Ex19":0,"R20":0,"Ex20":0,"R21":0,"Ex21":0}
#         budget[dept] = {"Revenues":0,"Expenses":0}
#         # budget[dept] = {"2019":0,"2020":0,"2021":0}
#     if not budget[dept].get(unit,''):
#         # budget[dept][unit] = {"2019":0,"2020":0,"2021":0}
#         budget[dept][unit] = {"Revenues":0,"Expenses":0}
#     budget[dept][type] += amount
#     budget[dept][unit][type] += amount
# for department, value in budget.items():
#     print('------\n')
#     print(department,"\t","R: ",value["Revenues"],"\t","E: ",value["Expenses"])
#     for unit, details in value.items():
#         if unit in ['Revenues','Expenses']:
#             continue
#         print('-->  ',unit,"\t","R: ",details["Revenues"],"\t","E: ",details["Expenses"])
#
# # funds = {"Revenues":[],"Expenses":[]}
# # for index, row in bdf.iterrows():
# #     # print(index)
# #     # print(row["Fund"])
# #     # print(row["Account Type"])
# #     # print(1/0)
# #     if row["Fund"] not in funds[row["Account Type"]]:
# #         funds[row["Account Type"]].append(row["Fund"])
# # for key, value in funds.items():
# #     print("-----\n")
# #     print(key)
# #     print(value)
# #     print("\n")
# # print(1/0)
#
#
#
# # for account in accounts:
# #     # budget[account] = {}
# #     for col in bdf:
# #         if col in accounts:
# #             continue
# #         elif col in ["2019 Adopted Budget","2020 Adopted Budget","2021 Projected Budget"]:
# #             continue
# #         if not budget.get(col,''):
# #             budget[col] = {"same":False,"Revenues":[],"Expenses":[]}
# #         budget[col][account] = bdf[col].unique()
# #         # if not budget[col][account].all():
# #         #     print(bdf[col].unique())
# #         #     print("Wump")
# #         # else:
# #         #     print(col,account)
# #         #     print(bdf[col].unique())
# #         if np.array_equal(budget[col]["Revenues"],budget[col]["Expenses"]):
# #             budget[col]["same"] = True
# #         else:
# #             budget[col]["same"] = False
# # for column, value in budget.items():
# #     print("-----\n")
# #     print(column)
# #     if value["same"]:
# #         print(value["Revenues"])
# #     else:
# #         print("~Revenues")
# #         print(value["Revenues"])
# #         print("\n")
# #         print("~Expenses")
# #         print(value["Expenses"])
