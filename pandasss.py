import pandas as pd
df = pd.read_csv("task.csv")


# ãÑÍáå ÇáÊÍæíá æÊäÖíİ ÇáÏÇÊÇ 
print(df.duplicated().sum())# 4 ÊßÑÇÑÇÊ
df.drop_duplicates(inplace=True)
df.dropna(how = "all",inplace=True,axis=0)# åÊãÓÍ ÇáÕİæİ Çáí ßáåÇİÇÖíå
df['Price'] = pd.to_numeric(df['Price'], errors ='coerce')# åÊÍæáåÇ áÇÑŞÇã
df['Price'] = df['Price'].abs()# åÊÍæá ÇáÇÑŞÇã ãä ÓÇáÈ áãæÌÈ
df['Quantity'] = pd.to_numeric(df['Quantity'], errors ='coerce')
df['Quantity'] = df['Quantity'].abs()#åÊÍæá ÇáÑŞã áãæÌÈ
df['Payment Method'] = df['Payment Method'].replace({"Creditcard" : "Credit Card",
"creditcard":"Credit Card",
"Cash":"Credit Card",
"E_Wallet":"Digital Wallet"})
df['Order Date'] = pd.to_datetime(df['Order Date'], errors="coerce")



#ãÑÍáå ÇáÊÚÏíá Úáí ÇáÏÇÊÇ æÊÚæíÖ ÇáŞíã ÇáãŞæÏå
df['Order Total'] = df['Order Total'].fillna(df['Price'] * df['Quantity'])#Úãáíå ÇÍÕÇÁíå áæ ÇáÓÚÑ æÇáßãíå ãæÌæÏí äåÊÚæÖ İí nall
df['Price'] = df['Price'].fillna(df['Order Total'] / df['Quantity'])
df['Quantity'] = df['Quantity'].fillna(df['Order Total'] / df['Price'])
df['Order Total'] = df['Order Total'].fillna(df['Order Total'].median())
df['Price'] = df['Price'].fillna(df['Price'].median())
df['Quantity'] = df['Quantity'].fillna(df['Quantity'].median())
df['Category'] = df['Category'].str.title().str.strip()#åÊÍæá ÚÇãæÏ Çáí Çæá ÍÑİ ßÇÈÊá æÊÔíá ÇáãÓÇİÇÊ
df['Payment Method'] = df['Payment Method'].str.title().str.strip()
df['Payment Method'] = df['Payment Method'].fillna(df['Payment Method'].mode()[0])#åÊÚæÖ İí ÇáŞíã ÇáãİŞæÏå ÈæÓíØ ÇáŞíã ÇáãæÌæÏå
df['Item'] = df['Item'].fillna(df['Item'].mode()[0])
df['Order Date'] = df['Order Date'].fillna(df['Order Date'].mode()[0])

print(df.isnull().sum())
print(df.iloc[4000:4050])
print(df[['Item','Price']])
print(df['Quantity'])
print(df.loc[1:50 , ['Price',"Item"]])
print(df.loc[1:50 , 'Price'])
print(df.iloc[1:50,[1,2]])
print(df.iloc[1:50,5])
print(df[df["Price"] > 10])
print(df[df['Quantity']> 3].sort_values(by='Quantity',ascending=False))
print(df.query("Price > 10").sort_values(by='Price'))
print(df.groupby('Item')['Quantity'].sum().sort_values(ascending=False)) #  ÇÚáí ÍÇÌå ÈíÔÊÑæåÇ åí ÇáÈÇÓÊÇ ÇáİÑíÏæ
print(df['Order Total'].describe()) # ÇÍÕÇÁ ÚÔÇä ÇáÚÇãæÏ ÇáÌÏíÏ
print(df.groupby('Quantity')['Order Total'].sum().sort_values(ascending = False))#ÇáØáÈÇÊ Çáí Êãáß ÇÚáí ÇÌãÇáí
# İßÑå ÇáÚÇãæÏ åíÚãá ãÓãí áßá ØáÈ Úáí ÎÓÈ ÇáÓÚÑ Çáßáí 
# åíİíÏ áãÇ äíÌí ãÚãá ÎÕã äÚãáå Úáí ÇáÇæÑÏÑ ÇáßÈíÑ ÈÓ
df['Order SIze'] = df['Order Total'].apply(lambda x : "Law" if x <= 24 else  ("Medium" if x  <= 70 else "High"))

print(df.head())
print(df.groupby("Item").agg({
    "Order Total" : ["sum","mean","count"],
    "Quantity" : "sum",
    "Price" : "mean"
 
}))

print(df.groupby("Category")['Order Total'].sum())# Desserts ÇÚáí ÇÌãÇáí ÇíÑÇÏÇÊ 
print(df.groupby('Item')['Quantity'].sum().sort_values(ascending=False)) #  ÇÚáí ÍÇÌå ÈíÔÊÑæåÇ åí ÇáÈÇÓÊÇ ÇáİÑíÏæ 
print(df.groupby("Item")['Order Total'].mean()) #ãÊæÓØ Şíãå ÇáØáÈ 
print(df.groupby("Customer ID")['Order Total'].sum().sort_values(ascending=False).head())#ÇÚáí ÎãÓ ÇÔÎÇÕ ÈíÕÑİæ 
print(df.groupby("Payment Method")['Order Total'].sum().sort_values(ascending=False)) #ÇÚáí ØÑíŞå ÏİÚ åí ßÑíÏÊ ßÇÑÏ 
print(df.groupby('Item')['Quantity'].sum().sort_values(ascending=False))#Pasta Alfredo   Side Salad      Ice Cream         Water     French Fries  

#ÇŞá ÍÇÌå ãÈíÚÇ æÈÊÏÎá İáæÓ ßÊíÑ Nachos Grande | #ÇáãÇíå ÇÚáí ÍÇÌå ÈÊÊÇÚ ÈÓ ÈİáæÓ Şáíáå æÏÇ ÈÓÈÈ ÇäåÇ ÑÎíÕå ÈÚÏåÇ ÇáÇíÓ ßÑíã
print(df.groupby("Item").agg({
    "Order Total" : "sum",
    "Quantity" : "sum"
}).sort_values(by="Order Total",ascending=False).sort_values(by='Quantity')) 

print(df.groupby("Payment Method")['Order Total'].sum().sort_values(ascending=False))









#1: Desert ÇáãØÚã ãÊÎÕÕ İíåÇ 
#2: pasta alfredo Şíãå ãŞÇÈá ÓÚÑ 
#3: ßÇÔ Èíßæä ÇßÊÑ ÇãÇä 
#4: ãÌÇæÈ Úáíå İæŞ 
#5:Main  Dishes áæ ÚäÕÑ ÇíÓ ßÑíã   áæ İÆå : 
#6: Cash Payment  äÓÈå ÇáÚãá ÈíåÇ Şáíáå
#7: ÇáÇåÊãÇã ÈÈÇŞí ÇáİÆÇÊ æäÙã ÇáÏİÚ
#final opinion: ÇáÎİÇÙ Úáí ŞÓã desert 
# pasta alfredo : deser
# main dishes : ice cream    

