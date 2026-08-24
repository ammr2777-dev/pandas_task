import pandas as pd
df = pd.read_csv("task.csv")


# مرحله التحويل وتنضيف الداتا 
df.dropna(how = "all",inplace=True,axis=0)# هتمسح الصفوف الي كلهافاضيه
df['Price'] = pd.to_numeric(df['Price'], errors ='coerce')# هتحولها لارقام
df['Price'] = df['Price'].abs()# هتحول الارقام من سالب لموجب
df['Quantity'] = pd.to_numeric(df['Quantity'], errors ='coerce')
df['Quantity'] = df['Quantity'].abs()#هتحول الرقم لموجب
df['Payment Method'] = df['Payment Method'].replace({"Creditcard" : "Credit Card",
"creditcard":"Credit Card",})
df['Order Date'] = pd.to_datetime(df['Order Date'], errors="coerce")
df['Category'] = df['Category'].replace({"Main  Dishes" :"Main Dishes"})
df['Category'] = df['Category'].str.title().str.strip()#هتحول عامود الي اول حرف كابتل وتشيل المسافات
df['Payment Method'] = df['Payment Method'].str.title().str.strip()
print(df.duplicated().sum())# 4 تكرارات
df.drop_duplicates(inplace=True)


#مرحله التعديل علي الداتا وتعويض القيم المقوده
df['Order Total'] = df['Order Total'].fillna(df['Price'] * df['Quantity'])#عمليه احصاءيه لو السعر والكميه موجودي نهتعوض في nall
df['Price'] = df['Price'].fillna(df['Order Total'] / df['Quantity'])
df['Quantity'] = df['Quantity'].fillna(df['Order Total'] / df['Price'])
df['Order Total'] = df['Order Total'].fillna(df.groupby('Item')['Order Total'].transform("median"))
df['Price'] = df['Price'].fillna(df.groupby('Item')['Price'].transform('median'))
df['Quantity'] = df['Quantity'].fillna(df.groupby('Item')['Quantity'].transform('median'))
df['Payment Method'] = df['Payment Method'].fillna(df['Payment Method'].mode()[0])#هتعوض في القيم المفقوده بوسيط القيم الموجوده
df['Item'] = df['Item'].fillna(df['Item'].mode()[0])
df['Order Date'] = df['Order Date'].fillna(df['Order Date'].mode()[0])
df.dropna(axis=0 , subset= ['Price','Quantity','Order Total'],inplace=True)

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
print(df.groupby('Item')['Quantity'].sum().sort_values(ascending=False)) #  اعلي حاجه بيشتروها هي باستا الفريدو
print(df.groupby('Quantity')['Order Total'].sum().sort_values(ascending = False))#الطلبات الي تملك اعلي اجمالي
# فكره العامود هيعمل مسمي لكل طلب علي خسب السعر الكلي 
# هيفيد لما نيجي معمل خصم نعمله علي الاوردر الكبير بس
df['Order Size'] = df['Order Total'].apply(lambda x : "Low" if x <= 24 else  ("Medium" if x  <= 70 else "High"))
df['Offer'] = df.apply(lambda x : x['Order Total'] * 0.20 if x['Order Size'] == "High" else  0 , axis= 1 ) 
print(df.head())
print(df.groupby("Item").agg({
    "Order Total" : ["sum","mean","count"],
    "Quantity" : "sum",
    "Price" : "mean"
 
}))

print(df.groupby("Category")['Order Total'].sum())# main dishes اعلي اجمالي ايرادات 
print(df.groupby('Item')['Quantity'].sum().sort_values(ascending=False)) #  اعلي حاجه بيشتروها هي باستا الفريدو  
print(df.groupby("Item")['Order Total'].mean()) #متوسط قيمه الطلب 
print(df.groupby("Customer ID")['Order Total'].sum().sort_values(ascending=False).head())#اعلي خمس اشخاص بيصرفو 
print(df.groupby("Payment Method")['Order Total'].sum().sort_values(ascending=False)) #اعلي طريقه دفع هي الكاش 
print(df.groupby('Item')['Quantity'].sum().sort_values(ascending=False))#Pasta Alfredo     Grilled Chicken    Steak   Salmon    Vegetarian Platter
#اقل حاجه مبيعا وبتدخل فلوس كتير Nachos Grande | #المايه اعلي حاجه بتتاع بس بفلوس قليله ودا بسبب انها رخيصه بعدها الايس كريم
print(df.groupby("Item").agg({
    "Order Total" : "sum",
    "Quantity" : "sum"
}).sort_values(by="Order Total",ascending=False).sort_values(by='Quantity')) 

print(df.columns)
print(df.groupby(df['Order Date'].dt.to_period("M"))['Order Total'].sum().sort_values(ascending=False))#2022-08  اعلي شهر في  ordar total
print(df.groupby(df['Order Date'].dt.to_period("M"))['Order Total'].count().sort_values(ascending=False))#022-08  اعلي شهر من حيث كميه الاوردرات
#1: Main Dishes المطعم متخصص فيها | الاكثر طلب
#2: باستا الفريدو | قيمه مقابل سعر | الاكثر طلبا
#3: كاش بيكون اكتر امان 
#4: مجاوب عليه فوق 
#5:Drinks لو عنصر ايس كريم   لو فئه : 
#6: E_wallet  نسبه العمل بيها قليله
#7: الاهتمام بباقي الفئات ونظم الدفع
#final opinion: الخفاظ علي قسم main dishes 
# pasta alfredo : main deshes
# drinks : ice cream    



#اقتراح ازاي نزود من استخدام دفع بالمحفظه الضعيفه هنخلي لو الاوردر مش تيك اواي لو دفع بالمحفظه الضغيفه نلغي الضريبه


#فكره العامودين الجداد ان احنا بنستهدف الفئه العاليه منها ممكن نعمل حاجات كتير زي خصم او هدايا او حتي نعرف اي الايتم الثابت بينه 
