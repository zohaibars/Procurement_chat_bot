from app.core.database import Database

class AnalysisService:
    @staticmethod
    def analyze_spending(source_documents):
        total_amount = 0
        purchases = []
        
        for doc in source_documents:
            try:
                price_str = doc.metadata.get('total_price', '0')
                if isinstance(price_str, str) and '$' in price_str:
                    price = float(price_str.replace('$', '').replace(',', ''))
                    total_amount += price
                    purchases.append({
                        'amount': price,
                        'date': doc.metadata.get('creation_date'),
                        'po': doc.metadata.get('purchase_order')
                    })
            except (ValueError, AttributeError):
                continue
        
        return {
            'total_amount': f"${total_amount:,.2f}",
            'num_purchases': len(purchases),
            'average_purchase': f"${(total_amount/len(purchases) if purchases else 0):,.2f}"
        }
    
    @staticmethod
    def get_summary_stats():
        collection = Database.connect()
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_orders": {"$sum": 1},
                    "unique_suppliers": {"$addToSet": "$Supplier Name"},
                    "unique_departments": {"$addToSet": "$Department Name"},
                    "total_spend": {
                        "$sum": {
                            "$convert": {
                                "input": {"$substr": ["$Total Price", 1, -1]},
                                "to": "decimal",
                                "onError": 0
                            }
                        }
                    }
                }
            }
        ]
        
        result = list(collection.aggregate(pipeline))[0]
        
        return {
            "total_orders": result["total_orders"],
            "total_suppliers": len(result["unique_suppliers"]),
            "total_departments": len(result["unique_departments"]),
            "total_spend": f"${result['total_spend']:,.2f}"
        }

analysis_service = AnalysisService()