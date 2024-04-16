<h1>MTG Card Generator</h1>
Tim Geoffrey & Luke Miller

<h3>How to use the system</h3>
<ol>
<li>Run run.exe 
    <ul><li>(I promise it is not a virus)</li></ul>
</li>
<li>Wait for it to load
    <ul><li>This may take a while because the executable contains all required python libraries and python itself</li></ul>
</li>
<li>Wait for it to initialize the required data
    <ul>
        <li>It ingests and parses a json file called 'en_card_file.json' within the data folder</li>
        <li>Currently, there is not functionality to load custom data files within the script</li>
    </ul>
</li>
<li>Decide whether you would like to train or load a model
    <ul>
        <li>Selecting train will immediately go into training and is a long process</li>
        <li>Training data is the parsed data from 'en_card_file.json'</li>
        <li>Selecting load will prompt you for the filename of a locally stored model. In this case, one is provided, and it is called 'prototype.h5'</li>
    </ul>
</li>
<li>After training or loading, it will go into predict mode, where you can generate card names
    <ul>
        <li>Follow on screen instructions</li>
        <li>The output/result of the prediction is displayed as a sentence</li>
        <li>TensorFlow may yell at you. This is fine and can be ignored.</li>
    </ul>
</li>
</ol>

<h3>Prototype Report</h3>

The final few lines of the training of 'prototype.h5':
<br><br>
19553/19553 [==============================] - 357s 18ms/step - loss: 2.0975 - accuracy: 0.5824 - SCA: 0.5824 - MSE: 15085207.0000 - RMSE: 3884.1123 - MAE: 2200.2329 - CS: 2.8048 - val_loss: 4.5367 - val_accuracy: 0.5158 - val_SCA: 0.5158 - val_MSE: 16873314.0000 - val_RMSE: 4107.6504 - val_MAE: 2300.4348 - val_CS: 3.1422
Model: "sequential"
_________________________________________________________________
 Layer (type)                Output Shape              Param #
=================================================================
 embedding (Embedding)       (None, 2, 100)            1834600

 lstm (LSTM)                 (None, 64)                42240

 dense (Dense)               (None, 64)                4160

 dropout (Dropout)           (None, 64)                0

 dense_1 (Dense)             (None, 18347)             1192555

=================================================================
Total params: 3,073,555
Trainable params: 3,073,555
Non-trainable params: 0
_________________________________________________________________

<br><br>
Important things to note here:
<ul>
    <li>Accuracy ~= 52%</li>
    <li>Root Mean Squared Error ~= 3900</li>
    <li>Mean Absolute Error ~= 2300</li>
    <li>Cosine Similarity ~= 3.14</li>
    <li># Layers = 5</li>
    <li>Total Parameters ~= 3.1M</li>
</ul>

No testing infrastructure has been developed yet. Obtaining precision, recall, and F1 score is not yet possible. Hopefully the aforementioned metrics can give a reasonable idea to the model's performance for now.
<br><br>
Was any overfitting identified? It is difficult to say. The data that was fed to this model has an impressively diverse vocabulary. I suspect that the model will have a difficult time generalizing when every document contains at least 1 unique token. Perhaps the goal is to not train it to a high degree of accuracy to reduce overfitting. Regardless, it still shows many signs of not having trained enough.
<br><br>
I would say that the model currently performs to a baseline acceptable degree. I argue it works quite well for a prototype. It performs well enough that, I wouldn't be heartbroken if this ended up being the final product for name generation. There are still some issues that should be addressed. Firstly, when generating more than 2 additional words, it really likes to repeat itself. Secondly, most names in MTG are fewer than 4 tokens long. I would like to figure out how to get our model to generate from essentially nothing, producing shorter names.