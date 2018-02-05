from rest_framework import permissions, generics
from rest_framework.decorators import api_view, permission_classes, detail_route, list_route
from rest_framework import mixins

from compounds import serializers
from compounds.models import *
from compounds.models import Compound_MS, Target, Drugs, Diseases, CompoundFirstCatagory, CompoundSecondCatagory, SubHerb
from compounds.models import TCMID_Herbs, ChEMBL, CHEMBLTarget
from compounds.models import Assay_Chembl_id, Doc_Chembl_id, Target_Chembl_id, Feedback
from dynamic_rest import viewsets
from rest_framework.response import Response
from django_rdkit.models import *
from rest_framework.permissions import AllowAny

class CompoundViewSet(viewsets.DynamicModelViewSet):
    queryset = Compound.objects.all()
    serializer_class = serializers.CompoundSerializer

    @list_route(methods=['POST', 'GET'], permission_classes=[permissions.AllowAny])
    def search(self, request):
        smiles = str(request.data['smiles'])
        similarity = float(request.data['similarity'])
        substructure_search = int(request.data['substructure_search'])
        # Perform substructure
        print(smiles, similarity, substructure_search)
        result = {}
        if substructure_search == 1:
            result = Compound.objects.filter(mol__hassubstruct=QMOL(Value(smiles))).all()
        # structure search
        else:
            try:
                result = Compound.objects.structure_search(smiles, similarity)
            except:
                print 'structure search error'

        if result:
            page = self.paginate_queryset(result)
            if page is not None:
                serializers = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializers.data)
            serializers = self.get_serializer(result, many=True)
            return Response(serializers.data)
        return Response(result)

class Compound_MSViewSet(viewsets.DynamicModelViewSet):
    queryset = Compound_MS.objects.all()
    serializer_class = serializers.Compound_MSSerializer


##### The target information comes from TCMID, it is not SEA prediction
class TargetViewSet(viewsets.DynamicModelViewSet):
    queryset = Target.objects.all()
    serializer_class = serializers.TargetSerializer

    # @list_route(methods=['POST', 'GET'], permission_classes=[permissions.AllowAny])
    # def search(self, request):
    #     English_name = request.data['English_name']


class DrugsViewSet(viewsets.DynamicModelViewSet):
    queryset = Drugs.objects.all()
    serializer_class = serializers.DrugsSerializer

class DiseasesViewSet(viewsets.DynamicModelViewSet):
    queryset = Diseases.objects.all()
    serializer_class = serializers.DiseasesSerializer

class CompoundFirstCategoryViewSet(viewsets.DynamicModelViewSet):
    queryset = CompoundFirstCatagory.objects.all()
    serializer_class = serializers.CompoundFirstCategorySerializer

class CompoundSecondCategoryViewSet(viewsets.DynamicModelViewSet):
    queryset = CompoundSecondCatagory.objects.all()
    serializer_class = serializers.CompoundSecondCategorySerializer

class HerbViewSet(viewsets.DynamicModelViewSet):
    queryset = Herb.objects.all()
    serializer_class = serializers.HerbSerializer

    # @list_route(methods=['POST', 'GET'], permission_classes=[permissions.AllowAny])
    # def search(self, request):
    #     English_name = request.data['English_name']
    #     Chinese_name = request.data['Chinese_name']


class SubHerbViewSet(viewsets.DynamicModelViewSet):
    queryset = SubHerb.objects.all()
    serializer_class = serializers.SubHerbSerializer

class TCMID_HerbsViewSet(viewsets.DynamicModelViewSet):
    queryset = TCMID_Herbs.objects.all()
    serializer_class = serializers.TCMID_HerbsSerializer

class PrescriptionViewSet(viewsets.DynamicModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = serializers.PrescriptionSerializer

    # @list_route(methods=['POST', 'GET'], permission_classes=[permissions.AllowAny])
    # def search(self, request):
    #     pass


###This is the same or similar chembl molecule with YaTCM
class ChEMBLViewSet(viewsets.DynamicModelViewSet):
    queryset = ChEMBL.objects.all()
    serializer_class = serializers.ChEMBLSerializer


### This is SEA prediction target of compound
class CHEMBLTargetViewSet(viewsets.DynamicModelViewSet):
    queryset = CHEMBLTarget.objects.all()
    serializer_class = serializers.CHEMBLTargetSerializer

class Assay_Chembl_idViewSet(viewsets.DynamicModelViewSet):
    queryset = Assay_Chembl_id.objects.all()
    serializer_class = serializers.Assay_Chembl_idSerializer

class Doc_Chembl_idViewSet(viewsets.DynamicModelViewSet):
    queryset = Doc_Chembl_id.objects.all()
    serializer_class = serializers.Doc_Chembl_idSerializer

class Target_Chembl_idViewSet(viewsets.DynamicModelViewSet):
    queryset = Target_Chembl_id.objects.all()
    serializer_class = serializers.Target_Chembl_idSerializer

class CIDViewSet(viewsets.DynamicModelViewSet):
    queryset = CID.objects.all()
    serializer_class = serializers.CIDSerializer

class CASViewSet(viewsets.DynamicModelViewSet):
    queryset = CAS.objects.all()
    serializer_class = serializers.CASSerializer

class KEGGPathwayCategoryViewSet(viewsets.DynamicModelViewSet):
    queryset = KEGGPathwayCategory.objects.all()
    serializer_class = serializers.KEGGPathwayCategorySerializer

class KEGGPathwayViewSet(viewsets.DynamicModelViewSet):
    queryset = KEGGPathway.objects.all()
    serializer_class = serializers.KEGGPathwaySerializer

class KEGGCompoundViewSet(viewsets.DynamicModelViewSet):
    queryset = KEGGCompound.objects.all()
    serializer_class = serializers.KEGGCompoundSerializer

class FeedbackCreateView(generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = serializers.FeedbackSerializer
    permission_classes = (AllowAny)



