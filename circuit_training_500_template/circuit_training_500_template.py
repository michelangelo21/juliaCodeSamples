#! /usr/bin/python3

import sys
import pennylane as qml
import numpy as np


def classify_data(X_train, Y_train, X_test):
    """Develop and train your very own variational quantum classifier.

    Use the provided training data to train your classifier. The code you write
    for this challenge should be completely contained within this function
    between the # QHACK # comment markers. The number of qubits, choice of
    variational ansatz, cost function, and optimization method are all to be
    developed by you in this function.

    Args:
        X_train (np.ndarray): An array of floats of size (250, 3) to be used as training data.
        Y_train (np.ndarray): An array of size (250,) which are the categorical labels
            associated to the training data. The categories are labeled by -1, 0, and 1.
        X_test (np.ndarray): An array of floats of (50, 3) to serve as testing data.

    Returns:
        str: The predicted categories of X_test, converted from a list of ints to a
            comma-separated string.
    """

    # Use this array to make a prediction for the labels of the data in X_test
    predictions = []

    # QHACK #
    # import torch.nn.functional as F
    # import torch
    num_wires = 1
    dev = qml.device("default.qubit", wires=num_wires)

    # YY = Y_train
    # y_train = np.zeros((Y_train.size, 3), dtype=np.float64)
    # y_train[np.arange(Y_train.size),Y_train+1] = 2
    # Y_train = y_train - 1 #onehot

    @qml.qnode(dev)
    def circuit(weights, x):
        for i in range(3):
            qml.RY(weights[i,0] * x[i] + weights[i,1], wires=0)
        return qml.expval(qml.PauliZ(0))

    def square_loss(labels, predictions):
        loss = 0
        for l, p in zip(labels, predictions):
            loss += (l-p)**2
        loss = loss / len(labels)
        return loss

    def cost(weights, features, labels):
        predictions = [(circuit(weights, f)) for f in features]
        loss = square_loss(labels, predictions)
        return loss

    weights = np.array([[1.0,0.0],[1.0,0.0],[1.0,0.0]], dtype=np.float64) # random

    np.random.seed(0)
    opt = qml.GradientDescentOptimizer(stepsize=0.1)
    batch_size = 30

    for it in range(20):
        batch_index = np.random.randint(0,len(Y_train), (batch_size,))
        X_batch = X_train[batch_index]
        Y_batch = Y_train[batch_index]
        weights = opt.step(lambda w: cost(w, X_batch, Y_batch), weights)

        #predictions_train = [variational_classifier(var,f) for f in X_train]
        #predictions_val = [variational_classifier(var,f) for f in X_test]

        # acc_train = cost(weights, X_train, Y_train)
        # print(it, acc_train)



    predictions = [circuit(weights,f) for f in X_test]
    
    for i in range(len(X_test)):
        if predictions[i] > 0.5:
            predictions[i] = 1
        elif predictions[i] < -0.5:
            predictions[i] = -1
        else:
            predictions[i] = 0

    # QHACK #

    return array_to_concatenated_string(predictions)


def array_to_concatenated_string(array):
    """DO NOT MODIFY THIS FUNCTION.

    Turns an array of integers into a concatenated string of integers
    separated by commas. (Inverse of concatenated_string_to_array).
    """
    return ",".join(str(x) for x in array)


def concatenated_string_to_array(string):
    """DO NOT MODIFY THIS FUNCTION.

    Turns a concatenated string of integers separated by commas into
    an array of integers. (Inverse of array_to_concatenated_string).
    """
    return np.array([int(x) for x in string.split(",")])


def parse_input(giant_string):
    """DO NOT MODIFY THIS FUNCTION.

    Parse the input data into 3 arrays: the training data, training labels,
    and testing data.

    Dimensions of the input data are:
      - X_train: (250, 3)
      - Y_train: (250,)
      - X_test:  (50, 3)
    """
    X_train_part, Y_train_part, X_test_part = giant_string.split("XXX")

    X_train_row_strings = X_train_part.split("S")
    X_train_rows = [[float(x) for x in row.split(",")] for row in X_train_row_strings]
    X_train = np.array(X_train_rows)

    Y_train = concatenated_string_to_array(Y_train_part)

    X_test_row_strings = X_test_part.split("S")
    X_test_rows = [[float(x) for x in row.split(",")] for row in X_test_row_strings]
    X_test = np.array(X_test_rows)

    return X_train, Y_train, X_test


if __name__ == "__main__":
    # # DO NOT MODIFY anything in this code block
    # X_train, Y_train, X_test = parse_input("0.46586604,0.47378893,0.22608081S0.32045034,0.26276939,0.12634708S-0.2470099,0.11383845,0.14686661S-0.39945595,0.12837791,0.16662385S-0.33023235,-0.12453634,0.19838102S0.0389054,-0.69261027,-1.21261411S0.42256658,0.14487072,0.35552406S0.0303721,-0.85336874,-1.18990811S-0.392693,0.19513864,0.17895097S0.18111608,-0.72151142,-0.95512507S-1.05264143e-03,-8.30227549e-01,-1.09879603e+00S0.03193414,-0.8447708,-1.02092673S0.19179465,-0.82053591,-1.11369488S0.07828842,-0.72121359,-1.03063612S-0.04261801,-0.83277986,-1.16934362S0.58582894,0.18689473,-0.0158016S0.47054132,0.45185067,0.11082881S-0.53220502,0.0745649,0.35702981S0.48842563,0.45346625,0.14954127S-0.5160971,0.19909077,0.2903203S0.05038535,-0.76699001,-1.07848612S-0.32660025,0.10945672,0.2024972S-0.5394994,0.22455073,0.20148256S0.5528424,0.31794484,0.09053302S0.47420368,0.33399085,-0.10304811S0.10312505,-0.7574786,-1.06435887S-0.62605291,0.06582095,0.36379447S0.31580511,0.32184123,-0.05351776S0.02968595,-0.91284674,-1.05289105S0.51966568,0.21633931,0.00648104S-0.07171478,-0.74513965,-1.15804761S0.40814842,0.45010358,0.05821922S0.04098097,-0.73361912,-1.10153893S0.05528618,-0.82638083,-0.99978546S0.55454061,0.33737905,0.01419551S-0.12677521,-0.75799267,-1.07740539S0.57376841,0.35411985,0.21902689S0.4628419,0.07548531,-0.01007068S-0.58499139,0.10132561,0.21754139S0.07461424,-0.77871035,-1.0814442S0.04051597,-0.72213868,-1.07933982S-0.45372273,0.3255691,0.33714207S0.03049757,-0.7809584,-1.21679712S0.71585987,0.22307051,-0.02668602S0.04026284,-0.89483754,-1.11810609S-0.6542349,0.02911683,0.18016644S-0.38597985,0.15599033,0.28498535S-0.60542281,-0.0215697,0.09006117S0.43969367,0.26848854,0.21111782S-0.01066465,-0.7473321,-1.02239483S0.38351869,0.44920541,-0.00296667S-0.67475164,0.10728927,0.25117917S0.43779221,0.31314116,0.12134041S-0.4990913,0.06831219,0.28735811S-0.56260046,0.08317784,0.10553639S-0.52682539,0.12420713,0.26004478S0.73364561,0.22928562,0.12229883S-0.0862039,-0.8800752,-1.3127185S0.57259556,0.05797397,0.1872531S-0.07674491,-0.78915102,-1.04782222S0.01081953,-0.68319945,-1.09432826S-0.49812869,0.16354196,0.19889403S-0.51589701,0.16000079,0.23662374S0.45003143,0.462059,-0.00046733S0.05196018,-0.86911901,-1.10572119S-0.09753183,-0.85924584,-1.2269797S-0.4387632,0.15434547,0.0945755S0.59692774,0.36828036,0.14479708S0.0945115,-1.00601545,-1.02386254S-0.02123672,-0.77908428,-0.91771505S-0.65315483,0.08252364,0.25992099S0.67920258,0.2535962,0.20332562S-0.51183021,0.33269296,0.02382962S0.03680035,-0.69996054,-1.2431507S0.093765,-0.82435502,-1.11777769S0.61758073,0.21074834,0.13390901S0.49244136,0.45368496,0.21100953S0.67153403,0.31335057,-0.0407779S-0.026173,-0.6268307,-1.0917989S-0.06618392,-0.82217384,-1.19868385S-0.59430397,-0.0392231,0.22348787S0.07648112,-0.89752536,-1.05764044S0.48571867,0.15742808,0.02545175S-0.52120387,0.05263318,0.05963792S0.46024834,0.46043696,0.1053023S0.43438268,0.18056089,0.34202475S-0.02439888,-0.85495369,-0.97373313S0.72267864,0.36271745,0.1392846S0.55364728,0.5956439,0.33923943S0.15663361,-1.01904261,-1.0090487S0.66453117,0.25252449,0.02474578S-0.01086562,-0.89226463,-1.13267025S0.61897491,0.49558478,0.11806663S-0.55912684,0.00742588,0.28311342S0.47177323,0.52614687,0.07675935S-0.12936416,-0.7821488,-1.08664497S0.61024675,0.14144255,0.03989248S-0.4507991,0.15829516,0.32716214S-0.08600944,-0.89287022,-0.99519577S-0.57401578,0.03659592,0.29150285S-0.61407857,0.09140983,0.1149462S-0.11362972,-0.73153221,-0.89771388S-0.649895,0.01662504,0.38531355S0.48865657,0.28472007,0.15177966S-0.4238432,0.08970976,0.15635289S-0.19565303,-0.83061094,-0.9649536S0.44306604,0.34002029,0.14302506S0.02977696,-0.86546233,-0.92870379S0.02677424,-0.81553439,-0.95730639S0.40994897,0.06150972,0.16046814S-0.07149889,-0.58208198,-1.0126174S-0.4659447,0.10283548,0.23093765S0.0874035,-0.69179745,-1.17117445S0.07873183,-0.66866557,-1.0784978S-0.48526743,0.14742026,0.27828786S0.09190276,-0.79045987,-1.05934517S0.50158225,0.16731197,0.16655285S-0.49948252,0.1593856,0.15049781S-0.31022551,-0.83829793,-1.10310754S-0.43075831,-0.06022182,-0.01180528S-0.14821455,-0.64819591,-1.07327132S0.43720573,0.46041497,0.01054351S0.04570713,-0.90472892,-0.89905817S-0.44126533,0.01203136,0.28900837S-0.45907141,0.11804302,0.08849841S0.48040568,0.25875523,0.04843328S0.01843911,-0.88741668,-1.19135387S0.58460096,0.34593132,-0.04856142S0.01384269,-0.73927445,-1.307374S0.00978928,-0.92487141,-1.08016442S0.4685007,0.15819096,-0.16311592S0.54811454,0.14682222,0.13901901S0.15005457,-0.67760829,-1.13745619S0.04058434,-0.85258189,-1.01363624S-0.44111201,0.30476937,0.17434411S-0.43616802,0.04681985,0.09555649S0.03431215,-0.93870912,-1.09438437S-0.52026004,0.14616853,0.25724309S-0.07031338,-0.82580299,-1.24194729S0.43817817,0.26749891,0.00132841S-0.39727368,0.36360971,0.27369237S0.33579518,0.25544255,0.16081367S0.29565719,0.45793857,0.0088813S-0.69896537,0.22678934,0.31350039S0.68222586,0.30100997,0.0437635S0.06622169,-0.85673734,-1.08118111S0.39282617,0.40234595,0.07506095S0.4857379,0.40896801,0.09344525S0.09212053,-0.72413501,-1.11650161S0.48557014,0.47273349,0.05720922S0.40308302,0.32246697,0.1064751S0.04940429,-0.85262005,-1.05449176S-0.5709479,0.03059745,0.04632767S-0.32793971,0.16124178,0.11995423S-0.38727553,-0.01855078,0.14433199S-0.57288858,0.05819425,0.2128305S-0.44641997,0.09128043,0.17438835S-0.5388403,0.19547007,0.19265951S-0.46334851,0.04242189,0.01612979S-0.09027154,-0.82974333,-1.2803292S0.35286716,0.22740138,0.10365117S-0.49228514,0.24978623,0.25686715S-0.5515381,0.20386659,0.30912911S0.15081505,-0.64879687,-0.93230771S0.37647883,0.22106232,0.18501978S-0.51215301,0.13692542,0.33482324S0.19329546,-0.74397745,-1.11249596S0.35472537,0.18899633,0.16715468S0.25607355,-0.68506018,-1.0159854S-0.05006557,-0.84420898,-1.04856424S-0.6696455,-0.07078573,0.25819087S-0.52644077,0.1145212,0.27219853S-0.12086319,-0.87598717,-1.07481487S-0.02347173,-0.69527117,-1.03966941S0.27546678,0.18010707,0.03962739S-0.50349136,0.03996178,0.28809504S0.361913,0.25842202,-0.04467126S-0.486705,-0.00678971,0.17854482S-0.0109565,-0.83968616,-1.18119864S-0.44638261,0.153507,0.17845016S0.07907108,-0.9432001,-1.24285891S-0.6350216,0.12039336,0.30715785S0.53217484,0.48816189,0.1367248S-0.60475111,0.08481663,0.23978851S-0.56765376,0.20918336,0.23348368S0.42801955,0.41959682,-0.02780118S0.4537108,0.29892194,-0.007192S-0.42762038,0.01964222,0.19056254S-0.14286424,-0.78978904,-1.20412948S0.06545285,-0.8167159,-1.22056366S0.59288922,0.51284355,0.15308085S-0.56120165,0.07225466,0.21966416S-0.3046686,0.05909879,0.35408052S0.4059693,0.26914838,0.13116571S-0.60878222,0.00358776,0.18593209S0.56745109,0.34224198,0.04420631S0.01543166,-0.8627333,-1.12044789S-0.59675659,0.28948505,0.00620695S-0.61216729,0.01620428,0.37048954S0.4687038,0.2360237,-0.07085847S-0.39932125,-0.01787135,0.1464044S-0.0779351,-0.97742816,-1.24662387S0.55342681,0.27456298,0.10023086S-0.52632321,0.03873461,0.25587369S0.60932188,0.26730498,0.08386286S-0.5468856,0.14761694,0.19828914S0.50265234,0.2803291,0.15565181S0.50242088,0.38989093,0.10242419S-0.47331057,0.02960588,0.20604749S-0.390229,0.24606526,0.27444132S0.07082366,-0.86312888,-1.15055461S-0.11870875,-0.89684984,-1.17832286S-0.00570379,-0.96989012,-1.15215462S-0.05258215,-0.85653616,-1.18856003S0.44722429,0.10055292,0.22554921S-0.46825365,0.18293021,0.26021155S-0.32421996,0.1153384,0.43635607S-0.44895139,-0.00675816,0.16446145S-0.02405064,-0.80741547,-1.14534244S-0.08678338,-0.79367383,-1.25331018S-0.01176539,-0.90345712,-1.06134848S0.60368723,0.26664392,0.21098173S0.59228637,0.25749427,-0.03103904S0.02343695,-0.67062437,-1.05584209S-0.47919673,0.12929776,0.27040821S0.43067021,0.24403681,0.18764622S-9.80510794e-04,-7.78606407e-01,-1.11240060e+00S-0.03937763,-0.77818193,-0.86033624S0.11202435,-0.82316473,-1.13125001S0.09485221,-0.72091877,-1.00720028S-0.03981215,-0.71906963,-1.28503853S0.48624908,0.17573623,0.06495013S-0.6050599,0.06255691,0.15804105S0.51627082,0.15613921,0.14858059S-0.64720412,0.0108199,0.2177732S-0.02710453,-0.9602563,-1.13461416S0.17018809,-0.81138114,-1.2630477S-0.61275141,0.16667063,0.08132574S-9.63246246e-04,-7.67162617e-01,-1.11932576e+00S-0.68456712,0.02955131,0.27780692S-0.48359735,0.09448787,0.19638433S-0.00616263,-0.67181641,-1.11448527S0.58366468,0.2620044,0.15242718S0.44313635,0.39350841,0.1859868S0.50905599,0.35109706,0.15049542S-0.00560399,-0.73204938,-1.00018059S0.61192557,0.41979195,0.12643753S0.46006123,0.45097321,-0.09123281S0.4417727,0.49338651,-0.02635283S-0.5145514,0.1683735,0.08893038XXX-1,-1,0,0,0,1,-1,1,0,1,1,1,1,1,1,-1,-1,0,-1,0,1,0,0,-1,-1,1,0,-1,1,-1,1,-1,1,1,-1,1,-1,-1,0,1,1,0,1,-1,1,0,0,0,-1,1,-1,0,-1,0,0,0,-1,1,-1,1,1,0,0,-1,1,1,0,-1,1,1,0,-1,0,1,1,-1,-1,-1,1,1,0,1,-1,0,-1,-1,1,-1,-1,1,-1,1,-1,0,-1,1,-1,0,1,0,0,1,0,-1,0,1,-1,1,1,-1,1,0,1,1,0,1,-1,0,1,0,1,-1,1,0,0,-1,1,-1,1,1,-1,-1,1,1,0,0,1,0,1,-1,0,-1,-1,0,-1,1,-1,-1,1,-1,-1,1,0,0,0,0,0,0,0,1,-1,0,0,1,-1,0,1,-1,1,1,0,0,1,1,-1,0,-1,0,1,0,1,0,-1,0,0,-1,-1,0,1,1,-1,0,0,-1,0,-1,1,0,0,-1,0,1,-1,0,-1,0,-1,-1,0,0,1,1,1,1,-1,0,0,0,1,1,1,-1,-1,1,0,-1,1,1,1,1,1,-1,0,-1,0,1,1,0,1,0,0,1,-1,-1,-1,1,-1,-1,-1,0XXX0.12689905,-0.7876047,-1.04365684S-0.52928694,0.11086547,0.20601985S0.5413154,0.3257977,-0.03238584S-0.43583611,0.13031294,0.29235773S0.66318733,0.17057945,0.25993422S0.13148431,-0.81582835,-1.04274795S0.45728263,0.39285875,0.06578703S0.55778387,0.17225289,-0.05135452S-0.47337053,0.13150477,0.25531901S0.37402566,0.2288446,0.29849314S-0.04105624,-0.88310185,-1.26749672S0.36695866,0.08880251,0.17892788S-0.48681198,0.18338072,0.26290681S-0.12915649,-0.94720221,-0.98128788S-0.36073185,0.11309875,0.16648451S0.40329104,0.32851071,0.10590837S0.53482868,0.35756364,0.05003754S-0.56117433,0.14090643,0.19954084S-0.48740957,-0.00051926,0.14699825S-0.07878229,-0.74275105,-1.11175667S0.06464298,-0.79461881,-1.33876567S-0.55054152,-0.07516366,0.11377265S0.60145565,0.22853613,0.00187534S-0.53967129,0.06017085,0.26616341S-0.46334692,0.13403597,0.32699485S0.45110893,0.31357292,0.10853206S-0.59676644,0.04037497,0.08384752S0.44793517,0.24868385,0.22297004S-0.40056483,0.04379854,0.23161959S-0.36317322,-0.00079074,0.23785054S0.25583087,-0.70569337,-1.1897083S0.00824735,-0.83002815,-1.10464594S0.57550495,0.32959665,0.1022398S0.7320316,0.3659234,0.18194847S0.46964819,0.30542544,0.19123075S-0.37876803,0.1077081,-0.04668136S0.37610909,0.42549055,0.14437636S-0.58397032,0.26809614,-0.00356644S0.10034199,-0.86862374,-1.28600421S-0.5804329,0.04154192,0.49486592S0.43392778,0.2090735,-0.03603803S0.26752925,-0.61200971,-1.00852761S0.02894648,-0.75668963,-1.14014966S-0.63152242,0.1417931,0.19207808S0.43507801,0.14127869,0.12733744S0.48594366,0.34472895,-0.02644236S0.41848143,0.4600378,0.25659156S0.61341124,0.23596843,0.23190163S-0.49730768,0.37092863,0.27156937S-0.55288172,0.18678882,0.02385478")

    X_train, Y_train, X_test = parse_input(sys.stdin.read())
    output_string = classify_data(X_train, Y_train, X_test)
    print(f"{output_string}")