items, vals, wts, capacity =  None, None, None, None
new_items = []
count = 0
for i in range(len(items)):
    for j in range(capacity//wts[i]):
        new_items.append(count)
        new_wts.append(wts[i])
        new_vals.append(vals[i])
        count+=1


