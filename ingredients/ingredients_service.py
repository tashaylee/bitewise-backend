import spacy
from spacy.lang.en.stop_words import STOP_WORDS

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")


class IngredientsService:
    def __init__(self) -> None:
        self.units = {
            'teaspoon', 'tsp',
            'tablespoon', 'tbsp',
            'fluid ounce', 'fl oz',
            'cup', 'c',
            'pint', 'pt',
            'quart', 'qt',
            'gallon', 'gal',
            'milliliter', 'ml',
            'liter', 'l',
            'ounce', 'oz',
            'pound', 'lb',
            'gram', 'g',
            'kilogram', 'kg',
            'each', 'ea',
            'piece', 'pc',
            'dozen', 'doz',
            'pinch',
            'dash',
            'scoop',
            'handful',
            'slice',
            'wedge',
            'clove',
            'sprig',
            'fahrenheit', '°f',
            'celsius', '°c'
        }
    
    def remove_units(self, ingr_list):
        # Check if any units are found from list of ingredients
        result = []
        for ingr in ingr_list:
            # Tokenize the ingredient using spaCy
            doc = nlp(ingr.lower())

            # Lemmatize the ingredient
            lemmatized_ingr = doc[0].lemma_ if doc else ingr.lower()

            # Check if the lemmatized ingredient is not in self.units
            if lemmatized_ingr not in self.units:
                result.append(ingr)

        return ''.join(result)
        
    def extract_ingredients(self, ingredient_list):
        ingredients = []

        for ingredient_text in ingredient_list:
            doc = nlp(ingredient_text)
            # Extract noun phrases as potential ingredient names
            ingredient_candidates = [
                token.text.lower()
                for token in doc
                if token.pos_ == "NOUN" or token.pos_ == "PROPN" or token.pos_ == "ADJ" or token.pos_ == "VERB"
            ]            # Filter out non-alphabetic phrases (remove measurements, quantities, etc.)
            ingredient_names = [phrase 
                                for phrase in ingredient_candidates 
                                if any(char.isalpha() for char in phrase) and all(char.isalnum() or char.isspace() for char in phrase)]
            cleaned_ingredient = self.remove_units(ingredient_names)
            # Add the identified ingredient names to the list
            ingredients.append(cleaned_ingredient)

        return ingredients

    def get_promo_price(self, price_data):
        promo_price = price_data.get('promo', None)
        regular_price = price_data.get('regular', None)

        if promo_price is not None and regular_price is not None:
            # Returns regular price when there is no promo happening
            if promo_price == 0:
                return regular_price
            else:
                return promo_price
        else:
            return None

    def preprocess_text(self, text):
        # Lowercase and remove stopwords
        doc = nlp(text.lower())
        preprocessed_text = ' '.join([token.text for token in doc if token.text not in STOP_WORDS])
        return preprocessed_text

    def extract_core_word(self, text):
        # Extract lemma (root form) of words
        doc = nlp(text)
        core_words = [token.lemma_ for token in doc]
        return ' '.join(core_words)

    def calculate_similarity(self, text1, text2):
        # Calculate similarity between preprocessed texts
        doc1 = nlp(text1)
        doc2 = nlp(text2)
        similarity_score = doc1.similarity(doc2)
        
        return similarity_score
    
    def related_ingredient(self, ingr_need, ingr_found):
        # Preprocess ingredients
        ingr_need = self.preprocess_text(ingr_need)
        ingr_found = self.preprocess_text(ingr_found)

        # Extract core words
        core_word_need = self.extract_core_word(ingr_need)
        core_word_found = self.extract_core_word(ingr_found)

        # Calculate similarity
        similarity_score = self.calculate_similarity(core_word_need, core_word_found)
        if similarity_score >= 0.5:
            return True
        return False

    
default = IngredientsService()