from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from .models import Port, Region, Price
import datetime
from .serializers import RateQuerySerializer, AveragePriceSerializer
from rest_framework.response import Response


class AveragePriceView(APIView):
    def get(self, request):
        serializer = RateQuerySerializer(data=request.GET)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        data = serializer.validated_data
        date_from = data['date_from']
        date_to = data['date_to']
        origin = data['origin']
        destination = data['destination']

        origin_ports = self.get_ports_for_slug_or_code(origin)
        destination_ports = self.get_ports_for_slug_or_code(destination)

        if not origin_ports or not destination_ports:
            return JsonResponse({'error': 'Invalid origin or destination'}, status=400)

        query = '''
                SELECT day, 
                       CASE WHEN COUNT(price) < 3 THEN NULL ELSE CAST(AVG(price) AS INTEGER) END AS average_price
                FROM prices
                WHERE orig_code IN %s 
                AND dest_code IN %s 
                AND day BETWEEN %s AND %s
                GROUP BY day
                ORDER BY day;
            '''
        with connection.cursor() as cursor:
            cursor.execute(query, [tuple(origin_ports), tuple(destination_ports), date_from, date_to])
            rows = cursor.fetchall()

        result = [{'day': row[0], 'average_price': row[1]} for row in rows]
        serializer = AveragePriceSerializer(data=result, many=True)

        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    # Both the origin, destination params accept either port codes or region slugs
    def get_ports_for_slug_or_code(self, slug_or_code):
        with connection.cursor() as cursor:
            # Check if the provided slug_or_code is a Region slug
            cursor.execute("SELECT slug FROM regions WHERE slug = %s", [slug_or_code])
            region_result = cursor.fetchall()

            if region_result:
                region_slug = region_result[0]
                # Retrieve subregions slugs for the given region
                cursor.execute("SELECT slug FROM regions WHERE parent_slug = %s", [region_slug])
                subregions_slugs = [row[0] for row in cursor.fetchall()]

                # Add the original region slug to the list of subregion slugs
                subregions_slugs.append(region_slug)

                # Get the port codes for all subregions including the original region
                if subregions_slugs:
                    cursor.execute("SELECT code FROM ports WHERE parent_slug IN %s", [tuple(subregions_slugs)])
                    ports = [row[0] for row in cursor.fetchall()]
                    return ports

            # Check if the provided slug_or_code is a Port code
            cursor.execute("SELECT code FROM ports WHERE code = %s", [slug_or_code])
            port_result = cursor.fetchone()

            if port_result:
                return [port_result[0]]

        return None

