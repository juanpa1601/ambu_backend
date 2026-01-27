from typing import Any
from django.db.models import Q
from django.db.models.query import QuerySet
from ..models import Diagnosis
from ..serializers.out import DiagnosisSerializer
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR
)

class ListDiagnosisApplicationService:
    '''
    Application service for listing and searching diagnoses (CIE-10 codes).
    
    Business logic:
    - Retrieve all active diagnoses
    - Search by CIE-10 code or diagnosis name
    - Order by CIE-10 code
    - Serialize data for API response
    '''
    
    SUCCESS: int = 1
    FAILURE: int = -1  

    def list_diagnoses(
        self, 
        search_query: str | None = None
    ) -> dict[str, Any]:
        '''    
        List or search diagnoses.
        
        Args:
            search_query: Optional search term to filter by code or name.
                         Minimum 2 characters required for search.
        
        Returns:
            dict: {
                'response': Success/error message
                'msg': 1 for success, -1 for error
                'status_code_http': HTTP status code
                'diagnoses': List of serialized diagnosis objects
                'total': Total count of diagnoses
                'search_applied': Boolean indicating if search was applied
            }
        
        Raises:
            Exception: If database query fails
        '''
        try:
            # Start with all diagnoses
            diagnoses: QuerySet[Diagnosis] = Diagnosis.objects.all()
            search_applied: bool = False
            # Apply search filter if query provided and meets minimum length
            if search_query and len(search_query.strip()) >= 2:
                search_term = search_query.strip()
                diagnoses = diagnoses.filter(
                    Q(cie_10__icontains=search_term) | 
                    Q(cie_10_name__icontains=search_term)
                )
                search_applied = True
            # Order by CIE-10 code and limit results
            diagnoses = diagnoses.order_by('cie_10')
            # Limit to 10 results when search is applied (performance optimization)
            if search_applied:
                diagnoses = diagnoses[:10]
            # Serialize data
            serializer: DiagnosisSerializer = DiagnosisSerializer(
                diagnoses, 
                many=True
            )
            return {
                'response': 'Exito al recuperar los diagnósticos.',
                'msg': self.SUCCESS,
                'status_code_http': HTTP_200_OK,
                'diagnoses': serializer.data,
                'total': len(serializer.data),
                'search_applied': search_applied,
                'search_query': search_query if search_applied else None
            }
        except Exception as e:
            return {
                'response': f'Error al recuperar los diagnósticos: {str(e)}',
                'msg': self.FAILURE,
                'status_code_http': HTTP_500_INTERNAL_SERVER_ERROR
            }