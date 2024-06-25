# apartment-for-rent

Data quality issue:
price, bedrooms are not that accurate.
e.g. Index 99824

studio have bedrooms 1 or 0.

## Feature Engineering

### Property features
How to deal with studio? bedrooms 0 or 1?

**square_feet**

### Geographical features

**latitude & longitude**

good to use

**state**

- Region Grouping: A common way of referring to regions in the United States is grouping them into 5 regions according to their geographic position on the continent: the Northeast, Southwest, West, Southeast, and Midwest. [ref](https://education.nationalgeographic.org/resource/united-states-regions/)
- Incorporating External Data: Include additional features such as state population, average income, or cost of living index to provide context. (next step)

**city name**
- Incorporating External Data: Include additional features such as city population, average income, or cost of living index to provide context. (next step)

This feature will not be use at current model. latitude & longitude already contains the info. 

### *Time feature
**time**

time series? trend?

