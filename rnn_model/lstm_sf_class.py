import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, LSTM
import json


class Lstm_sf(object):    
    def __init__(self, tsteps=2, lahead=1, batch_size=1, epochs=10, d_ticks='data_list_saved.json', d_names='stock_names_saved.json'):
        self.tsteps = tsteps
        self.lahead = lahead
        self.batch_size = batch_size
        self.epochs = epochs
        self.d_ticks = d_ticks
        self.d_names = d_names
        #np.random.seed(1986)
        self.to_drop = max(self.tsteps - 1, self.lahead - 1)



########################################

    def plot(self, symbol_list):
        self.data_ticks, self.data_names = self.data_loader()
        for ticker in symbol_list:
            self.state_test()
            data_input = pd.DataFrame(self.choose_symb(ticker)) 
            self.data_plotter(data_input, ticker)
    
            ########
            print('Creating Stateful Model...')
            model_stateful = self.create_model(stateful=True)        
            self.train_and_plot(data_input)
        
        pass


###################################################


    def data_loader(self):
        with open(self.d_ticks) as json_file1:
            data_ticks = json.load(json_file1)
        with open(self.d_names) as json_file2:
            data_names = json.load(json_file2)
        print('Files loaded')
        return data_ticks, data_names


    def state_test(self):
        print("*" * 33)
        if self.lahead >= self.tsteps:
            print("STATELESS LSTM WILL ALSO CONVERGE")
        else:
            print("STATELESS LSTM WILL NOT CONVERGE")
        print("*" * 33)
        pass

    def choose_symb(self, ticker_symb=['AAPL']):
        ''' 
        REQUIRES A VECTOR OF SYMBOLS (EVEN IF ONLY 1)
        Returns a matrix of serveral tickers 
        '''
        data_list = []
        num = 0
        # get number assigned to the symb name from data names
        for i in self.data_names[0]:
            if i == ticker_symb:
                num = i 
        # use number in outputting correct list from data_input
        for j in range(len(self.data_ticks[num])):
            data_list.append(self.data_ticks[num][j]['Open'])

        return data_list


        def data_plotter(self, data_input, ticker_symb):
            ''' drop the nan '''

            expected_output = data_input.rolling(window=self.tsteps, center=False).mean()

            # when lahead > 1, need to convert the input to "rolling window view"
            # https://docs.scipy.org/doc/numpy/reference/generated/numpy.repeat.html
            if self.lahead > 1:
                data_input = np.repeat(data_input.values, repeats=self.lahead, axis=1)
                data_input = pd.DataFrame(data_input)
                for i, c in enumerate(data_input.columns):
                    data_input[c] = data_input[c].shift(i)

            # drop the nan
            expected_output = expected_output[self.to_drop:]
            data_input = data_input[self.to_drop:]

            print('Input shape:', data_input.shape)
            print('Output shape:', expected_output.shape)
            print('Input head: ')
            print(data_input.head())
            print('Output head: ')
            print(expected_output.head())
            print('Input tail: ')
            print(data_input.tail())
            print('Output tail: ')
            print(expected_output.tail())

            print('Plotting input and expected output')
            plt.plot(data_input[0][:10], '.')
            plt.plot(expected_output[0][:10], '-')
            plt.legend([ticker_symb, 'Expected output'])
            plt.title(ticker_symb)
            #plt.show()
            plt.savefig(ticker_symb + '1.png')
            plt.close()    



            ######################




    def create_model(self, stateful: bool):
        model = Sequential()
        model.add(LSTM(20,
                input_shape=(self.lahead, 1),
                batch_size=self.batch_size,
                stateful=stateful))
        model.add(Dense(1))
        model.compile(loss='mse', optimizer='adam')
        return model


    # split train/test data
def split_data(self, x, y, ratio: int = 0.8):
    to_train = int(len(x) * ratio)
    # tweak to match with batch_size
    to_train -= to_train % self.batch_size

    x_train = x[:self.to_train]
    y_train = y[:self.to_train]
    x_test = x[self.to_train:]
    y_test = y[self.to_train:]

    # tweak to match with batch_size
    to_drop = x.shape[0] % self.batch_size
    if to_drop > 0:
        x_test = x_test[:-1 * to_drop]
        y_test = y_test[:-1 * to_drop]

    # some reshaping
    reshape_3 = lambda x: x.values.reshape((x.shape[0], x.shape[1], 1))
    x_train = reshape_3(x_train)
    x_test = reshape_3(x_test)

    reshape_2 = lambda x: x.values.reshape((x.shape[0], 1))
    y_train = reshape_2(y_train)
    y_test = reshape_2(y_test)

    return (x_train, y_train), (x_test, y_test)


    def train_and_plot(self, data_input):
        expected_output = data_input.rolling(window=self.tsteps, center=False).mean()
        (x_train, y_train), (x_test, y_test) = self.split_data(data_input, expected_output)
        for i in range(self.epochs):
            #print('Epoch', i + 1, '/', epochs)
            # Note that the last state for sample i in a batch will
            # be used as initial state for sample i in the next batch.
            # Thus we are simultaneously training on batch_size series with
            # lower resolution than the original series contained in data_input.
            # Each of these series are offset by one step and can be
            # extracted with data_input[i::batch_size].
            model_stateful.fit(x_train,
                            y_train,
                            batch_size=self.batch_size,
                            epochs=1,
                            verbose=1,
                            validation_data=(x_test, y_test),
                            shuffle=False)
            model_stateful.reset_states()

        #print('Predicting')
        predicted_stateful = model_stateful.predict(x_test, batch_size=self.batch_size)

        print('Creating Stateless Model...')
        model_stateless = create_model(stateful=False)

        print('Training')
        model_stateless.fit(x_train,
                            y_train,
                            batch_size=self.batch_size,
                            epochs=self.epochs,
                            verbose=1,
                            validation_data=(x_test, y_test),
                            shuffle=False)

        print('Predicting')
        predicted_stateless = model_stateless.predict(x_test, batch_size=self.batch_size)

        # ----------------------------

        print('Plotting Results')
        plt.subplot(3, 1, 1)
        plt.plot(y_test)
        plt.title('Expected')
        plt.subplot(3, 1, 2)
        # drop the first "tsteps-1" because it is not possible to predict them
        # since the "previous" timesteps to use do not exist
        plt.plot((y_test - predicted_stateful).flatten()[tsteps - 1:])
        plt.title('Stateful: Expected - Predicted')
        plt.subplot(3, 1, 3)
        plt.plot((y_test - predicted_stateless).flatten())
        plt.title('Stateless: Expected - Predicted')
        #plt.show()
        plt.savefig(ticker + '2.png')
        plt.close()