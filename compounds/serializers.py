from . import models
from dynamic_rest import serializers
from rest_framework.permissions import AllowAny

class EnglishIdentitySerializer(serializers.DynamicModelSerializer):
    class Meta:
        model = models.EnglishIdentity
        exclude = []

class ChineseIdentitySerializer(serializers.DynamicModelSerializer):
    class Meta:
        model = models.ChineseIdentity
        exclude = []


class CompoundSerializer(serializers.DynamicModelSerializer):
    chembls = serializers.DynamicRelationField('ChEMBLSerializer', many=True, deferred=True, embed=True)
    related_ChEMBL_targets = serializers.DynamicRelationField('CHEMBLTargetSerializer', many=True, deferred=True, embed=True)
    related_compounds = serializers.DynamicRelationField('CompoundSerializer', many=True, deferred=True, embed=True)
    compound_ms_set = serializers.DynamicRelationField('Compound_MSSerializer', many=True, deferred=True, embed=True)
    target_set = serializers.DynamicRelationField('TargetSerializer', many=True, deferred=True, embed=True)
    compoundfirstcategory_set = serializers.DynamicRelationField('CompoundFirstCategorySerializer', many=True, deferred=True, embed=True)
    compoundsecondcategory_set = serializers.DynamicRelationField('CompoundSecondCategorySerializer', many=True, deferred=True, embed=True)
    herb_set = serializers.DynamicRelationField('HerbSerializer', many=True, deferred=True, embed=True)
    tcmid_herbs_set = serializers.DynamicRelationField('TCMID_HerbsSerializer', many=True, deferred=True, embed=True)
    keggcompound_set = serializers.DynamicRelationField('KEGGCompoundSerializer', many=True, deferred=True, embed=True)
    keggsimilarity_set = serializers.DynamicRelationField('KEGGSimilaritySerializer', many=True, deferred=True, embed=True)



    class Meta:
        model = models.Compound
        exclude = ['bfp', 'mol', 'mol_block']

class Compound_MSSerializer(serializers.DynamicModelSerializer):
    compound = serializers.DynamicRelationField('CompoundSerializer', many=True, deferred=True, embed=True)

    class Meta:
        model = models.Compound_MS
        exclude = []

class TargetSerializer(serializers.DynamicModelSerializer):
    related_drugs = serializers.DynamicRelationField('DrugsSerializer', many=True, deferred=True, embed=True)
    related_diseases = serializers.DynamicRelationField('DiseasesSerializer', many=True, deferred=True, embed=True)
    compounds = serializers.DynamicRelationField('CompoundSerializer', many=True, deferred=True, embed=True)

    class Meta:
        model = models.Target
        exclude = []

class DrugsSerializer(serializers.DynamicModelSerializer):
    class Meta:
        model = models.Drugs
        exclude = []

class DiseasesSerializer(serializers.DynamicModelSerializer):
    target_set = serializers.DynamicRelationField('TargetSerializer', many=True, deferred=True, embed=True)

    class Meta:
        model = models.Diseases
        exclude = []

class CompoundFirstCategorySerializer(serializers.DynamicModelSerializer):
    compounds = serializers.DynamicRelationField('CompoundSerializer', many=True, deferred=True, embed=True)
    compoundsecondcategory_set = serializers.DynamicRelationField('CompoundSecondCategorySerializer', many=True, deferred=True, embed=True)
    class Meta:
        model = models.CompoundFirstCatagory
        exclude = []

class CompoundSecondCategorySerializer(serializers.DynamicModelSerializer):
    compounds = serializers.DynamicRelationField('CompoundSerializer', many=True, deferred=True, embed=True)
    first_category = serializers.DynamicRelationField('CompoundSerializer', many=True, deferred=True, embed=True)

    class Meta:
        model = models.CompoundSecondCatagory
        exclude = []

class HerbSerializer(serializers.DynamicModelSerializer):
    related_herbs = serializers.DynamicRelationField('HerbSerializer', many=True, deferred=True, embed=True)
    compounds = serializers.DynamicRelationField('CompoundSerializer', many=True, deferred=True, embed=True)
    subherb_set = serializers.DynamicRelationField('SubHerbSerializer', many=True, deferred=True, embed=True)
    # taxonomy = serializers.DynamicRelationField('TaxonomySerializer', many=True, deferred=True, embed=True)

    class Meta:
        model = models.Herb
        exclude = ['taxonomy']

class SubHerbSerializer(serializers.DynamicModelSerializer):
    herb = serializers.DynamicRelationField('HerbSerializer', many=True, deferred=True, embed=True)

    class Meta:
        model = models.SubHerb
        exclude = ['taxonomy']

class TCMID_HerbsSerializer(serializers.DynamicModelSerializer):
    compounds = serializers.DynamicRelationField('CompoundSerializer', many=True, deferred=True, embed=True)

    class Meta:
        model = models.TCMID_Herbs
        exclude = []

class PrescriptionSerializer(serializers.DynamicModelSerializer):
    herbs = serializers.DynamicRelationField('HerbSerializer', many=True, deferred=True, embed=True)
    main_prescription = serializers.DynamicRelationField('PrescriptionSerializer', many=True, deferred=True, embed=True)

    class Meta:
        model = models.Prescription
        exclude = []

class ChEMBLSerializer(serializers.DynamicModelSerializer):
    compound_set = serializers.DynamicRelationField('CompoundSerializer', many=True, deferred=True, embed=True)
    assay_chembl_ids = serializers.DynamicRelationField('Assay_Chembl_idSerializer', many=True, deferred=True, embed=True)
    doc_chembl_ids = serializers.DynamicRelationField('Doc_Chembl_idSerializer', many=True, deferred=True, embed=True)
    target_chembl_ids = serializers.DynamicRelationField('Target_Chembl_idSerializer', many=True, deferred=True, embed=True)

    class Meta:
        model = models.ChEMBL
        exclude = []

class Assay_Chembl_idSerializer(serializers.DynamicModelSerializer):
    chembl_set = serializers.DynamicRelationField('ChEMBLSerializer', many=True, deferred=True, embed=True)
    class Meta:
        model = models.Assay_Chembl_id
        exclude = []

class Doc_Chembl_idSerializer(serializers.DynamicModelSerializer):
    chembl_set = serializers.DynamicRelationField('ChEMBLSerializer', many=True, deferred=True, embed=True)
    class Meta:
        model = models.Doc_Chembl_id
        exclude = []

class Target_Chembl_idSerializer(serializers.DynamicModelSerializer):
    chembl_set = serializers.DynamicRelationField('ChEMBLSerializer', many=True, deferred=True, embed=True)
    class Meta:
        model = models.Target_Chembl_id
        exclude = []


class CHEMBLTargetSerializer(serializers.DynamicModelSerializer):
    compound_set = serializers.DynamicRelationField('CompoundSerializer', many=True, deferred=True, embed=True)

    class Meta:
        model = models.CHEMBLTarget
        exclude = []

class CIDSerializer(serializers.DynamicModelSerializer):
    compound = serializers.DynamicRelationField('CompoundSerializer', many=True, deferred=True, embed=True)

    class Meta:
        model = models.CID
        exclude = []

class CASSerializer(serializers.DynamicModelSerializer):
    compound = serializers.DynamicRelationField('CompoundSerializer', many=True, deferred=True, embed=True)

    class Meta:
        model = models.CAS
        exclude = []

class KEGGPathwayCategorySerializer(serializers.DynamicModelSerializer):
    Keggpathway_set = serializers.DynamicRelationField('KEGGPathwaySerializer', many=True, deferred=True, embed=True)
    class Meta:
        model = models.KEGGPathwayCategory
        exclude = []

class KEGGPathwaySerializer(serializers.DynamicModelSerializer):
    category = serializers.DynamicRelationField('KEGGPathwayCategorySerializer', many=True, deferred=True, embed=True)
    keggcompound_set = serializers.DynamicRelationField('KEGGCompoundSerializer', many=True, deferred=True, embed=True)

    class Meta:
        model = models.KEGGPathway
        exclude = []

class KEGGCompoundSerializer(serializers.DynamicModelSerializer):
    pathway = serializers.DynamicRelationField('KEGGPathwaySerializer', many=True, deferred=True, embed=True)
    similar_to_tcm = serializers.DynamicRelationField('CompoundSerializer', many=True, deferred=True, embed=True)
    keggsimilarity_set = serializers.DynamicRelationField('KEGGSimilaritySerializer', many=True, deferred=True, embed=True)

    class Meta:
        model = models.KEGGCompound
        exclude = ['mol', 'mol_block']

class KEGGSimilaritySerializer(serializers.DynamicModelSerializer):
    tcm = serializers.DynamicRelationField('CompoundSerializer', many=True, deferred=True, embed=True)
    kegg_compound = serializers.DynamicRelationField('KEGGCompoundSerializer', many=True, deferred=True, embed=True)

    class Meta:
        model = models.KEGGSimilarity
        exclude = []

class FeedbackSerializer(serializers.DynamicModelSerializer):
    class Meta:
        model = models.Feedback
        exclude = []


