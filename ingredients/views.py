from ingredients.serializers import IngredientSerializer
from .models import Ingredient
from .serializers import IngredientSerializer
from shared.serializers import UserSerializer
from store.serializers import StoreSerializer
from shared.models import User
from store.models import Store
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status


class IngredientView(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

    def create(self, request, *args, **kwargs):
        ingredients_data = request.data.get('ingredients', [])
        store_data = request.data.get('storeId', None)
        user_data = request.data.get('user', {})

        # Check if store or user already exists
        store, user = None, None
        if store_data or user_data:
            try:
                store = Store.objects.get(name=store_data)
                user_phone = user_data.get('phone')
                user = User.objects.get(phone=user_phone)
            except (Store.DoesNotExist, User.DoesNotExist):
                pass

        errors = {}

        # Validate and create Store and User
        if not store:
            store_serializer = StoreSerializer(data={'name': store_data})

            if store_serializer.is_valid():
                store = store_serializer.save()
            else:
                errors['store_errors'] = store_serializer.errors
        
        if not user:
            user_serializer = UserSerializer(data=user_data)

            if user_serializer.is_valid():
                user= user_serializer.save()
            else:
                errors['user_errors'] = user_serializer.errors


        if any(errors):
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
        
        ingredient_ids = []
        
        for ingredient_data in ingredients_data:
            ingredient_prices = ingredient_data.get('ingredient_prices', [])

            # Gets the description in ingredient_prices
            for price_data in ingredient_prices:
                description = price_data.get('description')
                # Use the description to set the name attribute of the Ingredient
                ingredient_name = description

                # Serialize ingredient
                ingredient_serializer = IngredientSerializer(
                    data={'name': ingredient_name, 'store': store.pk, 'user': user.pk}
                )

                if ingredient_serializer.is_valid():
                    ingredient = ingredient_serializer.save()
                    ingredient_ids.append(ingredient.id)
        
        return Response({'ingredient_ids': ingredient_ids}, status=status.HTTP_201_CREATED)
