import hashlib
import binascii

def home_mod_expnoent(x, y, n):
    # x^y % n
    resultat = 1
    x = x % n
    while y > 0:
        if y % 2 == 1:
            resultat = (resultat * x) % n
        y = y // 2
        x = (x * x) % n
    return resultat



def home_ext_euclide(y, b):
    a1, a2, a3 = 1, 0, y
    b1, b2, b3 = 0, 1, b
    while True:
        if b3 == 0:
            return a3
        if b3 == 1:
            return b2
        q = a3 // b3
        t1, t2, t3 = a1 - q * b1, a2 - q * b2, a3 - q * b3
        a1, a2, a3 = b1, b2, b3
        b1, b2, b3 = t1, t2, t3



def home_pgcd(a,b): #recherche du pgcd
    if(b==0): 
        return a 
    else: 
        return home_pgcd(b,a%b)



def home_string_to_int(x): # pour transformer un string en int
    z=0
    for i in reversed(range(len(x))):
        z=int(ord(x[i]))*pow(2,(8*i))+z
    return(z)



def home_int_to_string(x): # pour transformer un int en string
    txt=''
    res1=x
    while res1>0:
        res=res1%(pow(2,8))
        res1=(res1-res)//(pow(2,8))
        txt=txt+chr(res)
    return txt



def mot10char(): #entrer le secret
    secret=input("donner un secret de 10 caractères au maximum : ")
    while (len(secret)>11):
        secret=input("c'est beaucoup trop long, 10 caractères S.V.P : ")
    return(secret)



def CRT(xi, xj, d, c, n):
    p = max(xi, xj)
    q = min(xi, xj)
    inv_q = home_ext_euclide(p, q) # q^-1
    dq = home_mod_expnoent(d, 1, (q-1)) #dq
    dp = home_mod_expnoent(d, 1, (p-1)) #dp
    mq = home_mod_expnoent(c, dq, q)
    mp = home_mod_expnoent(c, dp, p)
    h = home_mod_expnoent((((mp - mq)) * inv_q), 1, p)
    m = home_mod_expnoent((mq + h*q), 1, n)
    
    return m
    


def main():
    #voici les éléments de la clé d'Alice
    x1a=7629726037683340809053781301491052450903774696953640341584051231729511370379166360126409803221117123 #p
    x2a=8363655490175461917767868789427975623690693529579788555091444824311849262262236116059668047613888361 #q
    na=x1a*x2a  #n
    phia=((x1a-1)*(x2a-1))//home_pgcd(x1a-1,x2a-1)
    ea=65537 #exposant public
    da=home_ext_euclide(phia,ea) #exposant privé
    #voici les éléments de la clé de bob
    x1b=1099574839562278306064474283355448461332374062045181832660087732634718557396781568567210505711041857 #p
    x2b=4979882905343183355397178910495211912545039962516000340728727490133703128519702970841414312070613091 #q
    nb=x1b*x2b # n
    phib=((x1b-1)*(x2b-1))//home_pgcd(x1b-1,x2b-1)
    eb=65537 # exposants public
    db=home_ext_euclide(phib,eb) #exposant privé



    print("Vous êtes Bob, vous souhaitez envoyer un secret à Alice")
    print("voici votre clé publique que tout le monde a le droit de consulter")
    print("n =",nb)
    print("exposant :",eb)
    print("voici votre précieux secret")
    print("d =",db)
    print("*******************************************************************")
    print("Voici aussi la clé publique d'Alice que tout le monde peut conslter")
    print("n =",na)
    print("exposent :",ea)
    print("*******************************************************************")
    print("il est temps de lui envoyer votre secret ")
    print("*******************************************************************")
    x=input("appuyer sur entrer")
    secret=mot10char()
    print("*******************************************************************")
    print("voici la version en nombre décimal de ",secret," : ")
    num_sec=home_string_to_int(secret)
    print(num_sec)
    print("voici le message chiffré avec la publique d'Alice : ")
    chif=home_mod_expnoent(num_sec, ea, na)
    print(chif)
    print("*******************************************************************")
    print("On utilise la fonction de hashage MD5 pour obtenir le hash du message",secret)
    Bhachis0=hashlib.sha256(secret.encode(encoding='UTF-8')).digest()#.md5(secret.encode(encoding='UTF-8',errors='strict')).digest() #MD5 du message
    print("voici le hash en nombre décimal ")
    Bhachis1=binascii.b2a_uu(Bhachis0)
    Bhachis2=Bhachis1.decode() #en string
    Bhachis3=home_string_to_int(Bhachis2)
    print(Bhachis3)
    print("voici la signature avec la clé privée de Bob du hachis")
    signe=home_mod_expnoent(Bhachis3, db, nb)
    print(signe)
    print("*******************************************************************")
    print("Bob envoie \n \t 1-le message chiffré avec la clé public d'Alice \n",chif,"\n \t 2-et le hash signé \n",signe)
    print("*******************************************************************")
    x=input("appuyer sur entrer")
    print("*******************************************************************")
    print("Alice déchiffre le message chiffré \n",chif,"\nce qui donne ")
    dechif=home_int_to_string(CRT(x1a, x2a, da, chif, na))#()home_mod_expnoent(chif, da, na)
    print(dechif)
    print("*******************************************************************")
    print("Alice déchiffre la signature de Bob \n",signe,"\n ce qui donne  en décimal")
    designe=CRT(x1b, x2b, eb, signe, nb)#home_mod_expnoent(signe, eb, nb)
    print(designe)
    print("Alice vérifie si elle obtient la même chose avec le hash de ",dechif)
    Ahachis0=hashlib.sha256(dechif.encode(encoding='UTF-8')).digest()#.md5(dechif.encode(encoding='UTF-8',errors='strict')).digest()
    Ahachis1=binascii.b2a_uu(Ahachis0)
    Ahachis2=Ahachis1.decode()
    Ahachis3=home_string_to_int(Ahachis2)
    print(Ahachis3)
    print("La différence =",Ahachis3-designe)
    if (Ahachis3-designe==0):
        print("Alice : Bob m'a envoyé : ",dechif)
    else:
        print("oups")