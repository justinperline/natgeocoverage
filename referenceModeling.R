data <- read.csv("~/Downloads/NatGeo/countryReferences.csv")

data <- subset(data, countryCode != 'USA')
data <- subset(data, countryCode != 'PRK')
data <- subset(data, countryCode != 'KOR')
data <- subset(data, countryCode != 'COD')
data <- subset(data, countryCode != 'COG')

popModel <- lm(numReferences ~ population, data=data)
summary(popModel)
